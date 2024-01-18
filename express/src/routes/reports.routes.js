import { Router } from "express";
import { getReports, getReport, createReports, updateReports, deleteReports } from "../controllers/reports.controller.js"
import { verifyToken, isModerator, isAdmin, isAdminOrModerator } from "../middlewares/authJwt.js";

const reportsRouter = Router()

reportsRouter.get('/', getReports);
reportsRouter.post('/', [verifyToken, isAdminOrModerator], createReports);
reportsRouter.put('/:id', [verifyToken, isAdminOrModerator], updateReports);
reportsRouter.delete('/:id', [verifyToken, isAdmin], deleteReports);
reportsRouter.get('/:id', getReport);

export default reportsRouter;