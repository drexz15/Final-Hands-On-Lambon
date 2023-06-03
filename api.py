from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL
import xml.etree.ElementTree as ET
import xml.dom.minidom

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "sakila"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data


@app.route("/country", methods=["GET"])
def get_country():
    data = data_fetch("""select * from country""")
    return make_response(jsonify(data), 200)


@app.route("/country/<int:id>", methods=["GET"])
def get_country_by_id(id):
    data = data_fetch("""SELECT * FROM country where country_id = {}""".format(id))
    return make_response(jsonify(data), 200)


@app.route("/country/store", methods=["GET"])
def get_country_by_store():
    data = data_fetch(
        """
        SELECT
    store.store_id,
    address.address,
    city.city,
    country.country
FROM
    store
INNER JOIN address ON store.address_id = address.address_id
INNER JOIN city ON address.city_id = city.city_id
INNER JOIN country ON city.country_id = country.country_id;
    """
    )
    return make_response(
        jsonify(data), 200)

@app.route("/country", methods=["POST"])
def add_country():
    info = request.get_json()
    cur = mysql.connection.cursor()
    country = info["country"]
    cur.execute("""INSERT INTO country (country) VALUES (%s);""", (country,))

    mysql.connection.commit()
    cur.close()
    return make_response(
        jsonify({"message": "country added successfully"}),201)

@app.route("/country/<int:id>", methods=["PUT"])
def update_country(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    country = info["country"]
    cur.execute(
    """UPDATE country SET country = %s WHERE country_id = %s;""",
    (country, id)
)

    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "country updated successfully", "rows_affected": rows_affected}
        ),
        201,
    )


@app.route("/country/<int:id>", methods=["DELETE"])
def delete_country(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM country where country_id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "country deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@app.route("/country/format", methods=["GET"])
def get_params():
    fmt = request.args.get('id')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format":fmt, "foo":foo}),200)


@app.route("/actors", methods=["POST"])
def add_actor():
    cur = mysql.connection.cursor()
    info = request.get_json()
    first_name = info["country"]
    cur.execute(
        """ INSERT INTO country (country) VALUE (%s)""",
        (first_name),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "country added successfully", "rows_affected": rows_affected}
        ),
        201,
    )
if __name__ == "__main__":
    app.run(debug=True)