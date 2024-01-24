// dependencia.js
import { DataTypes } from 'sequelize';
import { sequelize } from '../database/database.js';
import { DependenciaPrincipal } from './DependenciaPrincipal.js';

export const Dependencia = sequelize.define('dependencia', {
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

Dependencia.belongsTo(DependenciaPrincipal, { foreignKey: 'dependenciaPrincipalId' });