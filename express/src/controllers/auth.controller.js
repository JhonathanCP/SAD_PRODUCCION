import jwt from "jsonwebtoken";
import { User } from "../models/User.js"
import { Role } from "../models/Role.js"
import { SECRET } from "../config.js";

export const signupHandler = async (req, res) => {
    try {
        const { username, password, correo, nombres, apellidos, dni, area, red, roles } = req.body;

        // Creating a new User Object
        const newUser = await User.create({
            username,
            password,
            correo,
            nombres,
            apellidos,
            dni,
            area,
            red,
        });

        // checking for roles
        if (roles) {
            const foundRoles = await Role.findAll({ where: { nombre: roles } });
            await newUser.setRoles(foundRoles);
        } else {
            const role = await Role.findOne({ where: { nombre: "user" } });
            await newUser.setRoles([role]);
        }

        // Create a token
        const token = jwt.sign({ id: newUser.id, username: newUser.username }, SECRET, {
            expiresIn: "7200s", // 24 hours
        });

        return res.status(200).json({ token });
    } catch (error) {
        console.error(error);
        return res.status(500).json({ message: error.message });
    }
};

export const signinHandler = async (req, res) => {
    try {
        // Request body email can be an email or username
        const userFound = await User.findOne({
            where: { username: req.body.username },
            include: [{ model: Role, as: "roles" }],
        });

        if (!userFound) return res.status(400).json({ message: "User Not Found" });

        const matchPassword = await userFound.comparePassword(req.body.password);

        if (!matchPassword)
            return res.status(401).json({
                token: null,
                message: "Invalid Password",
            });
        
        const roles = await userFound.getRoles();

        const token = jwt.sign({ id: userFound.id, username: userFound.username, rol: roles[0].nombre }, SECRET, {
            expiresIn: "7200s", // 24 hours
        });

        res.json({ token });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: error.message });
    }
};