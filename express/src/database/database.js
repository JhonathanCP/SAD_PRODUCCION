import { Sequelize } from "sequelize";

export const sequelize = new Sequelize('pbi_gctic', 'postgres', 'AKindOfMagic', {
    host: '10.0.1.229',
    dialect: 'postgres',
//    dialectOptions: {
//       ssl: true
//      }
})
