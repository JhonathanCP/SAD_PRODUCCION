import express from "express";
import cors from "cors";
import morgan from "morgan";
import helmet from "helmet";
import groupsRouter from "./routes/groups.routes.js"
import reportsRouter from "./routes/reports.routes.js"
import authRouter from "./routes/auth.routes.js"
import usersRoutes from "./routes/user.routes.js";
import solicitudRoutes from './routes/solicitud.routes.js';
import {createRoles, createAdmin} from "./libs/initialSetup.js"
import path from "path"

const app = express();
createRoles();
createAdmin();

//middlewares
app.use(
    cors()
);
// app.use((req, res, next) => {
//   res.header('Access-Control-Allow-Origin', '*');
//   res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
//   res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
//   next();
// });

app.use(express.json());
app.use(helmet());
app.use(morgan('dev'));

app.use('/groups',groupsRouter)
app.use('/reports',reportsRouter)
app.use('/auth', authRouter)
app.use('/user', usersRoutes)
app.use('/solicitudes', solicitudRoutes);

// Archivos estáticos
const __dirname = path.dirname(new URL(import.meta.url).pathname);
app.use('/solicitudes', express.static(path.join(__dirname, 'solicitudes')));

// app.get('/', (req, res) => {
//   res.sendFile(path.join(__dirname, 'solicitudes', 'index.html'));
// });

export default app;
