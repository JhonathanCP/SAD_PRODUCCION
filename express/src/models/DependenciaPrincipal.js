// dependenciaPrincipal.js
import { DataTypes } from 'sequelize';
import { sequelize } from '../database/database.js';

export const DependenciaPrincipal = sequelize.define('dependenciaPrincipal', {
    id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true,
        allowNull: false,
    },
    codigo: {
        type: DataTypes.STRING,
    },
    descripcion: {
        type: DataTypes.STRING,
    },
}, {
    timestamps: false,
});