import { getClient, transaction } from "./db-client.mjs";
import format from "pg-format";
import { secretManager } from "./secret-manager.mjs";

const SCHEMA = "public";
const TABLE = "factura";

/**
 * body: {
 * fecha: string,
 * total: number,
 * detalles: [
 *  {
 *    nombre_producto: string,
 *    cantidad: number,
 *    precio: number
 *  }
 * ]
 * }
 */

export const handler = async (event, context) => {
  // TODO implement

  console.log("a ver si peta antes del secret manager");
  const dbcredentialsResult = await secretManager();
  console.log("dbcredentialsResult", dbcredentialsResult);

  if (event.httpMethod !== "GET") {
    throw new Error(
      `getMethod only accept GET method, you tried: ${event.httpMethod}`
    );
  }

  console.info("received:", event);
  let client;
  try {
    client = getClient();
    await client.connect();
    console.info("connected to database");

    const transactionResult = transaction(client, async () => {
      const body = JSON.parse(event.body);

      const facturaQuery = `insert into ${SCHEMA}.factura (fecha, total) values ($1, $2) returning id_factura;`;

      const values = [new Date(body.fecha), body.total];

      const facturaResult = await client.query(facturaQuery, values);
      const id_factura = facturaResult.rows[0].id_factura;

      if (!id_factura) {
        return {
          statusCode: 500,
          body: JSON.stringify("Error al insertar factura"),
        };
      }

      if (!body.detalles || body.detalles.length === 0) {
        return {
          statusCode: 500,
          body: JSON.stringify("Error detalles are empty"),
        };
      }

      const detalles = body.detalles.map((detalle) => {
        return [
          id_factura,
          detalle.nombre_producto,
          detalle.cantidad,
          detalle.precio,
        ];
      });

      const detalleQuery = format(
        `insert into ${SCHEMA}.detalle_factura (id_factura, nombre_producto, cantidad, precio) values %L`,
        detalles
      );

      const detalleResult = await client.query(detalleQuery);

      if (detalleResult?.rows?.length !== body?.detalles?.length) {
        return {
          statusCode: 500,
          body: JSON.stringify("Error al insertar detalles"),
        };
      }

      return detalleResult.rows;
    });

    if (transactionResult.error) {
      return {
        statusCode: 500,
        body: JSON.stringify(transactionResult.error),
      };
    }

    return {
      statusCode: 200,
      body: JSON.stringify(transactionResult.result),
    };
  } catch (err) {
    console.error("connection error", err);
    return {
      statusCode: 500,
      body: JSON.stringify(err),
    };
  } finally {
    client?.end();
  }
};
