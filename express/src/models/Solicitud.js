// solicitud.js
import { DataTypes } from 'sequelize';
import { sequelize } from '../database/database.js';
import { Group } from './Group.js';
import { Report } from './Report.js';
import { DependenciaPrincipal } from '../models/DependenciaPrincipal.js'; // Importa el modelo DependenciaPrincipal
import { Dependencia } from '../models/Dependencia.js'; // Importa el modelo Dependencia

export const Solicitud = sequelize.define('solicitud', {
    id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true,
        allowNull: false,
    },
    dni: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true,
    },
    correo: {
        type: DataTypes.STRING,
        validate: {
            isEmail: true,
        },
        allowNull: false,
    },
    nombres: {
        type: DataTypes.STRING,
    },
    apellidos: {
        type: DataTypes.STRING,
    },
    estado: {
        type: DataTypes.STRING,
    },
    cargo: {
        type: DataTypes.STRING,
    },
    nombreJefe: {
        type: DataTypes.STRING,
    },
    cargoJefe: {
        type: DataTypes.STRING,
    },
    celular: {
        type: DataTypes.STRING,
    },
    sustentoSolicitud: {
        type: DataTypes.STRING,
    },
    regimen: {
        type: DataTypes.STRING,
    },
    pdfContent: {
        type: DataTypes.BLOB('long'),
    },
    modulos: {
        type: DataTypes.STRING,
    },
    reportes: {
        type: DataTypes.STRING,
    }
});

Solicitud.belongsTo(DependenciaPrincipal, { foreignKey: 'dependenciaPrincipalId' }); // Agrega esta línea
Solicitud.belongsTo(Dependencia, { foreignKey: 'dependenciaId' }); // Agrega esta línea