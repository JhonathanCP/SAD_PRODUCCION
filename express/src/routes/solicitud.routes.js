import express from 'express';
import {
    getAllSolicitudes,
    getSolicitudByDni,
    createSolicitud,
    updateSolicitud,
    deleteSolicitud,
    uploadPdfMiddleware,
    subirPdf
} from '../controllers/solicitud.controller.js';

const router = express.Router();

router.get('/', getAllSolicitudes);
router.get('/:dni', getSolicitudByDni);
router.post('/', createSolicitud);
router.post('/:id/pdf',uploadPdfMiddleware, subirPdf);  
router.put('/:dni', updateSolicitud);
router.delete('/:dni', deleteSolicitud);

export default router;
