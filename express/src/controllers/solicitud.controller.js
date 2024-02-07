// controllers/solicitudController.js

import { Solicitud } from '../models/Solicitud.js';
import multer from 'multer';

const storage = multer.memoryStorage();
const upload = multer({ storage: storage });


// Obtener todas las solicitudes
export const getAllSolicitudes = async (req, res) => {
    try {
        const solicitudes = await Solicitud.findAll();
        res.json(solicitudes);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al obtener las solicitudes.' });
    }
};

// Obtener una solicitud por su DNI
export const getSolicitudByDni = async (req, res) => {
    const { dni } = req.params;
    try {
        const solicitud = await Solicitud.findByPk(dni);
        if (solicitud) {
            res.json(solicitud);
        } else {
            res.status(404).json({ error: 'Solicitud no encontrada.' });
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al obtener la solicitud.' });
    }
};

// Crear una nueva solicitud sin el archivo PDF
export const createSolicitud = async (req, res) => {
    try {
        const solicitudData = req.body;
        solicitudData.estado = '0'
        // Crear la solicitud sin el PDF
        const nuevaSolicitud = await Solicitud.create(solicitudData);

        res.status(201).json(nuevaSolicitud);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al crear la solicitud.' });
    }
};

export const subirPdf = async (req, res) => {
    try {
        const { id } = req.params;

        // Verifica si el ID de la solicitud está presente
        if (!id) {
            return res.status(400).json({ error: 'Se requiere el ID de la solicitud.' });
        }

        // Obtener el contenido del archivo PDF desde req.file.buffer
        const pdfContent = req.file.buffer;

        // Asociar el contenido del PDF a la solicitud con el ID correspondiente
        const solicitud = await Solicitud.findByPk(id);
        if (solicitud) {
            solicitud.estado = '1';
            solicitud.pdfContent = pdfContent;
            await solicitud.save();

            return res.json({ message: 'PDF subido exitosamente.' });
        } else {
            return res.status(404).json({ error: 'Solicitud no encontrada.' });
        }
    } catch (error) {
        console.error(error);
        return res.status(500).json({ error: 'Error al subir el PDF.' });
    }
};

// Aplicar el middleware de multer para manejar la carga de archivos
export const uploadPdfMiddleware = upload.single('pdfFile');

// Aceptar una solicitud
export const acceptSolicitud = async (req, res) => {
    const { dni } = req.params;
    try {
        const solicitud = await Solicitud.findByPk(dni);
        if (solicitud) {
            // Verificar si la solicitud tiene el estado adecuado para ser aceptada
            if (solicitud.estado === '1') {
                solicitud.estado = '2';
                await solicitud.save();
                res.json(solicitud);
            } else {
                res.status(400).json({ error: 'La solicitud no está pendiente por aprobar.' });
            }
        } else {
            res.status(404).json({ error: 'Solicitud no encontrada.' });
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al aceptar la solicitud.' });
    }
};

export const denySolicitud = async (req, res) => {
    const { dni } = req.params;
    try {
        const solicitud = await Solicitud.findByPk(dni);
        if (solicitud) {
            // Verificar si la solicitud tiene el estado adecuado para ser aceptada
            if (solicitud.estado === '1') {
                solicitud.estado = '3';
                await solicitud.save();
                res.json(solicitud);
            } else {
                res.status(400).json({ error: 'La solicitud no está pendiente por aprobar.' });
            }
        } else {
            res.status(404).json({ error: 'Solicitud no encontrada.' });
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al aceptar la solicitud.' });
    }
};

// Actualizar una solicitud
export const updateSolicitud = async (req, res) => {
    const { dni } = req.params;
    const updatedData = req.body;
    try {
        const solicitud = await Solicitud.findByPk(dni);
        if (solicitud) {
            await solicitud.update(updatedData);
            res.json(solicitud);
        } else {
            res.status(404).json({ error: 'Solicitud no encontrada.' });
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al actualizar la solicitud.' });
    }
};

// Eliminar una solicitud
export const deleteSolicitud = async (req, res) => {
    const { dni } = req.params;
    try {
        const solicitud = await Solicitud.findByPk(dni);
        if (solicitud) {
            await solicitud.destroy();
            res.json({ message: 'Solicitud eliminada exitosamente.' });
        } else {
            res.status(404).json({ error: 'Solicitud no encontrada.' });
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al eliminar la solicitud.' });
    }
};