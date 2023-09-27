from __future__ import annotations
from abc import ABC, abstractmethod
from tabulate import tabulate
from enum import Enum, unique
import pyodbc


# -----------------------------------------------------------------------------
# PROXY: 1.- Service Interface
# -----------------------------------------------------------------------------
class ServiceInterface(ABC):
    """Clase interfaz de los servicios de consulta y conexión a la base de datos"""
    @abstractmethod
    def get_users(self) -> None:
        """Consulta y guarda en una tabla los datos de los usuarios y su código de
        autorización (nivel)"""
        pass

    @abstractmethod
    def logout(self) -> None:
        """Termina la sesión del usuario y cierra la conexión a MS SQL"""
        pass

    @abstractmethod
    def get_authorization(self) -> int:
        """Obtiene un nivel de autorización para un usuario específico"""
        pass

    @abstractmethod
    def get_business_partner(self, bp_code: str) -> None:
        """Consulta la base de datos por los datos básicos de un socio de negocio
        y los imprime en modo tabular"""
        pass

    @abstractmethod
    def get_invoice(self, doc_num: int) -> None:
        """Consulta la base de datos por los datos básicos de una factura y los
        imprime en modo tabular"""
        pass

# -----------------------------------------------------------------------------
# PROXY: 2.- Servicio original del cliente, con Patron creacional / Singleton
# -----------------------------------------------------------------------------
class MSSQL(ServiceInterface):
    """Clase del cliente para conexión y consulta de documentos a la base de
    MS SQL SERVER"""

    _INSTANCE: MSSQL = None

    def __init__(self, user: str, password: str):
        """Método que permite una única creación de la instancia singleton Session,
        ligada a una conexión a la base de datos. Solo en caso de no tener
        una session activa y de lograr una conexión exitosa guarda la única instancia.
            * Si se tenía una instancia activa muestra un mensaje de error.
            * Si no se logra una conexión exitosa a la base de datos muestra la
              correspondiente excepción."""

        if MSSQL._INSTANCE is None:
            self.__table_users = {}
            self.user = user
            # CONEXIÓN A DB MS SQL SERVER
            server = 'SAP'
            database = 'SBODemoMX'
            self.user = user
            self._password = password
            driver = 'DRIVER={ODBC Driver 17 for SQL Server}'
            try:
                self._connect = pyodbc.connect(driver +
                                               ';SERVER=' + server +
                                               ';DATABASE=' + database +
                                               ';UID=' + user +
                                               ';PWD=' + password)
                MSSQL._INSTANCE = self  # SINGLETON "LATCH"
                self.get_users()
                print(f'-I- {user}')
            except pyodbc.Error as ex:
                sqlstate = ex.args[1]
                print('-Exception- ' + sqlstate)
        else:
            print('-E- Ya existe un usuario en la sesión')


    @classmethod
    def get_instance(cls) -> MSSQL:
        """Devuelve la única instancia de la clase, representa un usuario-conexión"""
        return cls._INSTANCE

    def get_users(self) -> None:
        try:
            cursor = self._connect.cursor()
            sql = f"""
                SELECT
                PRINCIPAL_ID,
                NAME,
                CASE
                    WHEN NAME LIKE '%logis%' THEN 1
                    WHEN NAME LIKE '%finan%' THEN 2
                    WHEN NAME LIKE '%prof%' OR NAME LIKE '%admin%' THEN 3
                    ELSE 0
                END AS AUTH  
                FROM sys.sql_logins
                ORDER BY AUTH, NAME 
            """
            cursor.execute(sql)
            for row in cursor.fetchall():
                self.__table_users[row.NAME] = {
                    'id': row.PRINCIPAL_ID,
                    'authorization': row.AUTH
                }
            cursor.close()
        except pyodbc.Error as ex:
            sqlstate = ex.args[1]
            print('-Exception- ' + sqlstate)

    def logout(self) -> None:
        try:
            # DESCONEXIÓN A DB MS SQL SERVER
            self._connect.close()
            print(f'-LOGOUT- {self.user}')
            self.__table_users.clear()
            MSSQL._INSTANCE = None
        except pyodbc.Error as ex:
            sqlstate = ex.args[1]
            print('-Exception- ' + sqlstate)

    def get_authorization(self) -> int:
        return self.__table_users[self.user]['authorization']

    def get_business_partner(self, bp_code: str) -> None:
        sql = f"""
                SELECT 
                T0.[CardCode], 
                T0.[CardName], 
                T0.[CardType], 
                T0.[Address], 
                T0.[ZipCode], 
                T0.[BalanceSys] 
                FROM OCRD T0
                WHERE T0.[CardCode] = \'{bp_code}\';
            """
        self._print_sql(sql)

    def get_invoice(self, doc_num: int) -> None:
        sql = f"""
                SELECT T0.[DocNum], 
                T0.[CardName], 
                T1.[LineNum], 
                T1.[ItemCode], 
                T1.[Dscription], 
                T1.[Quantity], 
                T1.[PriceBefDi], 
                T1.[LineTotal] 
                FROM OINV T0  
                INNER JOIN INV1 T1 ON T0.[DocEntry] = T1.[DocEntry]
                WHERE T0.[DocNum] = \'{doc_num}\';
            """
        self._print_sql(sql)

    def _print_sql(self, sql: str) -> None:
        """Método auxiliar para imprimir en terminal el resultado de una consulta
        SQL, en modo tabular"""
        try:
            cursor = self._connect.cursor()
            cursor.execute(sql)
            print(tabulate(cursor.fetchall(),
                           [column[0] for column in cursor.description],
                           tablefmt='psql'))
            cursor.close()
        except pyodbc.Error as ex:
            sqlstate = ex.args[1]
            print('-Exception- ' + sqlstate)


# -----------------------------------------------------------------------------
# 3.- Proxy - Override
# -----------------------------------------------------------------------------
class Proxy(ServiceInterface):
    @unique
    class Authorization(Enum):
        """Niveles de autorización en función al tipo de usuario,
        ligado a tipos de licencias reales de SAP Business One"""
        OTHER = 0
        LOGISTIC = 1
        FINANCIAL = 2
        PROFESSIONAL = 3

    @unique
    class Operation(Enum):
        """Tipos de operaciones (consultas) hacia la base de datos"""
        BUSINESS_PARTNER = 0
        INVOICE = 1

    def __init__(self, database: MSSQL) -> None:
        """En este constructor se observa la agregación del servicio original
        tipo MSSQL"""
        self.__db = database

    def get_users(self) -> None:
        self.__db.get_users()

    def logout(self) -> None:
        self.__db.logout()

    def get_authorization(self) -> int:
        return self.__db.get_authorization()

    def get_business_partner(self, bp_code: str) -> None:
        if self.check_access(self.Operation.BUSINESS_PARTNER):
            self.__db.get_business_partner(bp_code)
        else:
            print('-E- Permisos insuficientes para obtener datos')
            return None

    def get_invoice(self, doc_num: int) -> None:
        if self.check_access(self.Operation.INVOICE):
            self.__db.get_invoice(doc_num)
        else:
            print('-E- Permisos insuficientes para obtener datos')
            return None

    def check_access(self, operation: Operation) -> bool:
        """Esta función permite cumplir con los nuevos requerimientos de control
        de acceso al definir reglas en función a las operaciones solicitadas y
        el usuario específico que desea realizarlas, concediendo o no el permiso"""
        if operation == self.Operation.BUSINESS_PARTNER:
            if self.__db.get_authorization() > self.Authorization.FINANCIAL.value:
                return True
            else:
                return False
        elif operation == self.Operation.INVOICE:
            if self.__db.get_authorization() >= self.Authorization.LOGISTIC.value:
                return True
            else:
                return False

