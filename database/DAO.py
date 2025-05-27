from database.DB_connect import DBConnect
from model.prodotto import Prodotto


class DAO():

    @staticmethod

    def getColori():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct gp.Product_color as color
                    from go_products gp"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["color"])
        cursor.close()
        conn.close()
        return result




    @staticmethod
    def getProducts():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct *
                        from go_products gp """

        cursor.execute(query)

        for row in cursor:
            result.append(Prodotto(row["Product_number"],
                                   row["Product_line"],
                                   row["Product_type"],
                                   row["Product"],
                                   row["Product_brand"],
                                   row["Product_color"],
                                   row["Unit_cost"],
                                   row["Unit_price"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(anno, color):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT COUNT(*) AS weight,
                        gds1.Product_number AS Product1,
                        gds2.Product_number AS Product2
                    FROM 
                        go_daily_sales gds1
                    JOIN go_daily_sales gds2 
                        ON gds1.Date = gds2.Date 
                        AND gds1.Retailer_code = gds2.Retailer_code
                        AND gds1.Product_number < gds2.Product_number
                    JOIN go_products gp1 ON gp1.Product_number = gds1.Product_number
                    JOIN go_products gp2 ON gp2.Product_number = gds2.Product_number
                    WHERE 
                        YEAR(gds1.Date) = %s
                        AND YEAR(gds2.Date) = %s
                        AND gp1.Product_color = %s
                        AND gp2.Product_color = %s
                    GROUP BY 
                        gds1.Product_number, gds2.Product_number;"""


        cursor.execute(query, (anno, anno, color, color))

        for row in cursor:
            result.append((row["Product1"], row["Product2"], row["weight"]) )
            print((row["Product1"], row["Product2"], row["weight"]))
        cursor.close()
        conn.close()
        return result