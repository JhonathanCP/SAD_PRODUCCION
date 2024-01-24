import app from "./app.js";
import { sequelize } from "./database/database.js"
import './models/Group.js'
import './models/Report.js'
import './models/User.js'
import './models/Role.js'
import './models/Solicitud.js'

async function main() {
    try {
        await sequelize.authenticate();
        await sequelize.sync({force: true});
        console.log('Database connected');
        app.listen(4000);
        console.log("Serven is listening on port", 4000);
    } catch (error) {
        console.log('Unable to connect to database', error);
    }
}

main();