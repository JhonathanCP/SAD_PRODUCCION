import { Router } from "express";
import { getGroups, getGroup, createGroups, updateGroups, deleteGroups, getGroupReports, getInfo } from "../controllers/groups.controller.js"
import { verifyToken, isModerator, isAdmin, isAdminOrModerator } from "../middlewares/authJwt.js";

const groupsRouter = Router()

groupsRouter.get('/', getGroups);
groupsRouter.post('/', [verifyToken, isAdminOrModerator], createGroups);
groupsRouter.get('/panel', [verifyToken], getInfo);
groupsRouter.put('/:id', [verifyToken, isAdminOrModerator],updateGroups);
groupsRouter.delete('/:id', [verifyToken, isAdmin],deleteGroups);
groupsRouter.get('/:id', getGroup);
groupsRouter.get('/:id/reports', getGroupReports);

export default groupsRouter;