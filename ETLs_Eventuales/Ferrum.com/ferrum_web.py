from sshtunnel import SSHTunnelForwarder
import pymysql
import paramiko
import pandas as pd
import csv
#bs4 yBeautifulSoup permiten detectar etiquetas html de los textos
from bs4 import BeautifulSoup

# Datos de conexión SSH
ssh_host = '44.205.103.70'
ssh_port = 22
ssh_user = 'ferrumcom_ro'
private_key_path = "C:/Users/thiag/F.V.S.A/Equipo BI - General/Proyectos Visual Studio/DW_OD_Eventuales/Ferrum.com/ferrumcom.key"

# Datos de conexión a la base de datos MySQL
mysql_host = '127.0.0.1'
mysql_port = 3336
mysql_database = 'ferrum_db'
mysql_user = 'ferrumcom_ro'
mysql_password = '65$%B#9td!dzSbDd'

# Cargar la clave privada desde el archivo .key
private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

try:
    # túnel SSH con la clave privada
    with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_pkey=private_key,
        remote_bind_address=(mysql_host, mysql_port)
    ) as tunnel:
        # Establecer la conexión a la base de datos MySQL a través del túnel SSH
        conexion_mysql = pymysql.connect(
            host=mysql_host,
            port=tunnel.local_bind_port,
            user=mysql_user,
            passwd=mysql_password,
            db=mysql_database
        )

        # consultas SQL en la base de datos MySQL
        
        # handel_proyects
        consulta_handel_proyects = 'SELECT id, customer_id, name FROM handel_proyects;'

        # proceso la query y la guardo
        df_handel_proyects = pd.read_sql_query(consulta_handel_proyects, con=conexion_mysql)
        
        # Limpieza de datos
        df_handel_proyects = df_handel_proyects.replace('\n', ' ', regex=True)
        df_handel_proyects_cleaned = df_handel_proyects.fillna('NULL')

        # Ruta del archivo CSV
        path_handel_proyects = "//fe-files01/DW_OnDemand/Ferrum.com/f_web_handel_proyects.csv"

        #exporto a csv
        df_handel_proyects_cleaned.to_csv(path_handel_proyects, index=False, quotechar='"', sep=';', quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8-sig')

        ###############################
         # customer_entity
        
        consulta_customer_entity = """
        SELECT 
            entity_id,
            website_id,
            email,
            group_id,
            increment_id,
            store_id,
            created_at,
            updated_at,
            is_active,
            disable_auto_group_change,
            created_in,prefix,
            firstname,
            middlename,
            lastname,
            suffix,
            dob,
            password_hash,
            rp_token,
            rp_token_created_at,
            default_billing,
            default_shipping,
            taxvat,
            confirmation,
            gender,
            failures_num,
            first_failure,
            lock_expires,
            session_cutoff,
            mp_smtp_email_marketing_synced 
        
        FROM customer_entity WHERE created_at >= CURRENT_TIMESTAMP - INTERVAL 5 DAY;
        """

        # proceso la query y la guardo
        df_customer_entity = pd.read_sql_query(consulta_customer_entity, con=conexion_mysql)
        
        # Limpieza de datos
        df_customer_entity = df_customer_entity.replace('\n', ' ', regex=True)
        df_customer_entity_cleaned = df_customer_entity.fillna('NULL')

        # Ruta del archivo CSV
        path_customer_entity = "//fe-files01/DW_OnDemand/Ferrum.com/f_web_customer_entity.csv"

        #exporto a csv
        df_customer_entity_cleaned.to_csv(path_customer_entity, index=False, quotechar='"', sep=';', quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8-sig')

        ################################

        # handel_proyects_products        
        
        consulta_handel_proyects_products = 'SELECT id, proyect_id, product_id FROM handel_proyects_products'

        # proceso la query y la guardo
        df_handel_proyects_products = pd.read_sql_query(consulta_handel_proyects_products, con=conexion_mysql)
        
        # Limpieza de datos
        df_handel_proyects_products = df_handel_proyects_products.replace('\n', ' ', regex=True)
        df_handel_proyects_products_cleaned = df_handel_proyects_products.fillna('NULL')

        # Ruta del archivo CSV
        path_handel_proyects_products = "//fe-files01/DW_OnDemand/Ferrum.com/f_web_handel_proyects_products.csv"

        #exporto a csv
        df_handel_proyects_products_cleaned.to_csv(path_handel_proyects_products, index=False, quotechar='"', sep=';', quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8-sig')

        ########################

        # catalog_product_flat_1    
        
        consulta_catalog_product_flat_1 = """
        SELECT 
            entity_id,
            attribute_set_id,
            type_id,
            acople_rapido,
            acople_rapido_value,
            agujeros,
            agujeros_value,
            altura,
            altura_unidad,
            altura_unidad_value,
            ancho,
            ancho_unidad,
            ancho_unidad_value,
            cantidad_puertas,
            cierre,
            cierre_value,
            componentes,
            cost,
            created_at,
            descarga_parcial,
            descarga_parcial_value,
            descarga_sistema,
            descarga_sistema_value,
            descarga_total,
            descarga_total_value,
            description,    
            espesor,
            espesor_unidad,
            espesor_unidad_value,
            forma,
            forma_value,
            garantia,
            garantia_value,
            garantia_casco,
            garantia_casco_value,
            garantia_electronica,
            garantia_electronica_value,
            garantia_mecanismo,
            garantia_mecanismo_value,
            garantia_motor,
            garantia_motor_value,
            gift_message_available,
            has_options,
            herraje,
            herraje_value,
            highlights,
            image,
            image_label,
            img_hover,
            incluye,
            jerarquia_3,
            jets,
            jets_value,
            linea,
            linea_value,
            line_page_order,
            links_exist,
            links_purchased_separately,
            material,
            material_value,
            msrp,
            msrp_display_actual_price_type,
            name,
            news_from_date,
            news_to_date,
            nivel_de_equipamiento,
            nivel_de_equipamiento_value,
            numero_de_cajones,
            origen,
            origen_value,
            patas_de_apoyo,
            pa_os,
            perfiles,
            peso,
            peso_unidad,
            peso_unidad_value,
            posicion_motor,
            posicion_motor_value,
            price,
            price_type,
            price_view,
            profundidad,
            profundidad_unidad,
            profundidad_unidad_value,
            rebalse,
            rebalse_value,
            required_options,
            segmento,
            segmento_value,
            short_description,
            sku,
            sku_type,
            small_image,
            small_image_label,
            special_from_date,
            special_price,
            special_to_date,
            swatch_image,
            tapas_imagen_inodoro,
            tapas_imagen_inodoro_value,
            tapa_ancho,
            tapa_entre,
            tapa_ino_ancho,
            tapa_ino_entre,
            tapa_ino_largo,
            tapa_largo,
            tapa_sku_inodoro_compatible,
            tax_class_id,
            thumbnail,
            thumbnail_label,
            tipo_de_instalacion,
            tipo_de_instalacion_value,
            tipo_de_mampara,
            tipo_de_mampara_value,
            tipo_funcionamiento,
            tipo_funcionamiento_value,
            updated_at,
            url_key,
            url_path,
            visibility,
            volumen,
            volumen_unidad,
            volumen_unidad_value,
            weight,
            weight_type
        FROM
            catalog_product_flat_1 WHERE created_at >= CURRENT_TIMESTAMP - INTERVAL 5 DAY;
        """

        # proceso la query y la guardo
        df_catalog_product_flat_1 = pd.read_sql_query(consulta_catalog_product_flat_1, con=conexion_mysql)
        
        # Limpieza de datos
        df_catalog_product_flat_1 = df_catalog_product_flat_1.replace('\n', ' ', regex=True)
        df_catalog_product_flat_1 = df_catalog_product_flat_1.fillna('NULL')
        # Limpiar la columna "description" eliminando las etiquetas HTML
        df_catalog_product_flat_1['description'] = df_catalog_product_flat_1['description'].apply(lambda x: BeautifulSoup(x, 'html.parser').get_text())

        # Ruta del archivo CSV
        path_catalog_product_flat_1 = "//fe-files01/DW_OnDemand/Ferrum.com/f_web_catalog_product_flat_1.csv"

        #exporto a csv
        df_catalog_product_flat_1.to_csv(path_catalog_product_flat_1, index=False, quotechar='"', sep=';', quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8-sig')

        ########################

        # handel_store_locations
        
        consulta_handel_store_locations = """
            SELECT id
                ,cod
                ,legal_name
                ,display_name
                ,address_1
                ,address_2
                ,region
                ,state
                ,locality
                ,city
                ,zip_code
                ,latitude
                ,longitude
                ,schedules
                ,email
                ,website
                ,phone
                ,whatsapp
                ,facebook
            FROM handel_store_locations
        """

        # proceso la query y la guardo
        df_handel_store_locations = pd.read_sql_query(consulta_handel_store_locations, con=conexion_mysql)
        
        # Limpieza de datos
        df_handel_store_locations = df_handel_store_locations.replace('\n', ' ', regex=True)
        df_handel_store_locations_cleaned = df_handel_store_locations.fillna('NULL')

        # Ruta del archivo CSV
        path_handel_store_locations = "//fe-files01/DW_OnDemand/Ferrum.com/f_web_handel_store_locations.csv"

        #exporto a csv
        df_handel_store_locations_cleaned.to_csv(path_handel_store_locations, index=False, quotechar='"', sep=';', quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8-sig')

finally:
    # Cerrar el cursor y la conexión con la base de datos MySQL
    if 'conexion_mysql' in locals():
        conexion_mysql.close()
