import { log } from 'console';
import { Client } from 'pg';

export function getClient() {

	return new Client({
        database: process.env.DB_NAME,
        host: process.env.DB_HOST,
        port: parseInt(process.env.DB_PORT),
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD
    });
}

export async function transaction(client, func) {
	try {
		console.info("Beginning transaction...");
		await client.query("BEGIN");
		const result = await func();

		// This means is an HTTP response.
		if (result.response) {
			console.info("Rolling back transaction due to HTTP response...");
			await client.query("ROLLBACK");
			return result;
		}

		console.info("Comitting transaction...");
		await client.query("COMMIT");
		return { result };
	} catch (error) {
		console.error({ error }, "Rolling back transaction due to error...");
		await client.query("ROLLBACK");
		return { error };
	}
} 

