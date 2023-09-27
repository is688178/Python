from PySQL import MSSQL, Proxy

# -----------------------------------------------------------------------------
# PROXY: 4.- Cliente, puede utilizar tanto la clase MSSQL para compatibilidad
# como Proxy para mayor seguridad y nuevos requerimientos gracias a la interfaz
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    print('-INFO- Ejecución de inicios de sesión')
    s1 = MSSQL('admin', '688178')
    s2 = MSSQL('admin', 'incorrect_password')
    s1.get_users()
    s1.logout()
    s3 = MSSQL('admin', 'incorrect_password')
    s4 = MSSQL('inexistent_user', '688178')
    s5 = MSSQL('admin', '688178')
    s5.get_business_partner('C23900')
    s5.get_invoice(627)
    s5.logout()
    print('*' * 100 + '\n')

    print('-INFO- Ejecución de la consulta directamente usando el objeto MSSQL')
    db = MSSQL('logis01', 'logistica')
    db.get_business_partner('C23900')
    db.get_invoice(627)
    db.logout()
    print('*' * 100 + '\n')

    print('-INFO- Ejecución de la consulta usando un proxy - Autorización Logística')
    db2 = MSSQL('logis01', 'logistica')
    proxy = Proxy(db2)
    proxy.get_business_partner('C23900')
    proxy.get_invoice(627)
    proxy.logout()
    print('*' * 100 + '\n')

    print('-INFO- Ejecución de la consulta usando un proxy - Autorización Admin')
    db2 = MSSQL('admin', '688178')
    proxy = Proxy(db2)
    proxy.get_business_partner('C23900')
    proxy.get_invoice(627)
    print('*' * 100 + '\n')
