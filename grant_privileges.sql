-- 1. Asegúrate de estar en la base de datos correcta
\c pos_db

-- 2. Dale la propiedad del esquema al usuario
ALTER SCHEMA public OWNER TO pos_dev;

-- 3. Dale permisos explícitos sobre todas las tablas actuales
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO pos_dev;

-- 4. CRITICAL: Dale permisos sobre las SECUENCIAS (Para que funcione el SERIAL)
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO pos_dev;

-- 5. Asegura que las tablas que crees en el futuro también hereden estos permisos
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO pos_dev;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO pos_dev;


-- 1. Nos paramos en la base de datos
\c pos_db

-- 2. Aplicamos la regla para tablas futuras creadas por 'create_tables'
ALTER DEFAULT PRIVILEGES FOR USER pos_create IN SCHEMA public 
GRANT ALL PRIVILEGES ON TABLES TO pos_dev;

-- 3. Aplicamos lo mismo para las secuencias (los contadores SERIAL)
ALTER DEFAULT PRIVILEGES FOR USER pos_create IN SCHEMA public 
GRANT ALL PRIVILEGES ON SEQUENCES TO pos_dev;