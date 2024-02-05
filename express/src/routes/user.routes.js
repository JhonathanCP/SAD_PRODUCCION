import { Router } from "express";
import { createUser, getUser, getUsers, editUser, deleteUser, addGroupToUser, addReportToUser, addRoleToUser, removeGroupFromUser, removeReportFromUser, removeRoleFromUser, addAllPermissions } from "../controllers/user.controller.js";
import { isAdmin, isAdminOrModerator, verifyToken } from "../middlewares/authJwt.js";

const router = Router();

router.post("/", [verifyToken, isAdmin], createUser);
router.get("/", [verifyToken, isAdminOrModerator], getUsers);
router.put("/:userId", [verifyToken, isAdminOrModerator], editUser);
router.delete("/:userId", [verifyToken, isAdminOrModerator], deleteUser);
router.get("/:id", [verifyToken, isAdminOrModerator], getUser);
router.post("/:userId/roles/:roleId", [verifyToken, isAdminOrModerator], addRoleToUser);
router.post("/:userId/group/:groupId", [verifyToken, isAdminOrModerator], addGroupToUser);
router.post("/:userId/report/:reportId", [verifyToken, isAdminOrModerator], addReportToUser);
router.post("/:userId/addAll", [verifyToken, isAdminOrModerator], addAllPermissions);
router.delete("/:userId/roles/:roleId", [verifyToken, isAdminOrModerator], removeRoleFromUser);
router.delete("/:userId/group/:groupId", [verifyToken, isAdminOrModerator], removeGroupFromUser);
router.delete("/:userId/report/:reportId", [verifyToken, isAdminOrModerator], removeReportFromUser);

export default router;