import cx_Oracle

def update_ingredient_quantity(item_id):
    # Connect to Oracle Database
    conn = cx_Oracle.connect(user="system", password="thing1318", dsn="XE", encoding="UTF-8")
    cursor = conn.cursor()

    # PL/SQL block to update ingredient quantities and handle restock warnings
    plsql_block = """
        DECLARE
            l_quantity NUMBER;
            l_restock_warning CONSTANT NUMBER := 5;
            l_restock_quantity CONSTANT NUMBER := 10;
            CURSOR c_ingr IS
                SELECT ingr_id
                FROM made_of
                WHERE item_id = :item_id;
        BEGIN
            FOR r_ingr IN c_ingr LOOP
                -- Update ingredient quantity
                UPDATE ingredient
                SET quantity = quantity - 1
                WHERE ingr_id = r_ingr.ingr_id;

                -- Check if quantity is below restock warning threshold
                SELECT quantity INTO l_quantity
                FROM ingredient
                WHERE ingr_id = r_ingr.ingr_id;

                -- If below restock warning, restock ingredient quantity
                IF l_quantity < l_restock_warning THEN
                    UPDATE ingredient
                    SET quantity = l_restock_quantity
                    WHERE ingr_id = r_ingr.ingr_id;
                    COMMIT;
                    DBMS_OUTPUT.PUT_LINE('Ingredient restocked for ingr_id: ' || r_ingr.ingr_id);
                END IF;
            END LOOP;
        END;
    """
    cursor.execute(plsql_block, {'item_id': item_id})
    conn.commit()

    # Close database connection
    cursor.close()
    conn.close()
