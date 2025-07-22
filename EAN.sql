-- Recibe un código de 12 dígitos (como texto)--
-- Aplica la fórmula estándar del EAN-13 para calcular el dígito verificador (número 13)--
-- Devuelve el código completo de 13 dígitos (los 12 originales + el dígito verificador)--
CREATE OR REPLACE FUNCTION calcular_digito_ean13(codigo_base TEXT)
RETURNS TEXT AS $$
DECLARE
  suma INT := 0;
  i INT;
  digito INT;
BEGIN
  FOR i IN 1..12 LOOP
    digito := CAST(SUBSTRING(codigo_base, i, 1) AS INTEGER);
    IF i % 2 = 0 THEN
      suma := suma + digito * 3;
    ELSE
      suma := suma + digito;
    END IF;
  END LOOP;
  RETURN codigo_base || ((10 - (suma % 10)) % 10);
END;
$$ LANGUAGE plpgsql;


--Inserta los datos en la tabla codigos_barras--
INSERT INTO codigos_barras (producto_id, codigo, fecha)
SELECT 
  "ID",
  calcular_digito_ean13(LPAD(("ID" * 100)::text, 12, '0')),
  CURRENT_TIMESTAMP
FROM productos
WHERE "ID" IS NOT NULL
ORDER BY "ID";
