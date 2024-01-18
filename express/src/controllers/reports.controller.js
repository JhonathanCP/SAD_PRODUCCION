import { Report } from "../models/Report.js"

export const getReports = async (req, res) => {
    try {
        const reports = await Report.findAll()
        res.json(reports)
    } catch (error) {
        return res.status(500).json({message: error.message})
    }
}

export const getReport = async (req, res) => {
    try {
        const {id} = req.params
        const report = await Report.findByPk(id)
        res.json(report)
    } catch (error) {
        return res.status(500).json({message: error.message})
    }
}

export const createReports = async (req, res) => {
    try {
        const {nombre, descripcion, activo, link, groupId} = req.body
        const report = new Report()
        report.nombre = nombre  
        report.descripcion = descripcion
        report.activo = activo
        report.link = link
        report.groupId = groupId
        await report.save()
        res.json(report)
    } catch (error) {
        return res.status(500).json({message: error.message})
    }
}

export const updateReports = async (req, res) => {
    try {
        const {id} = req.params
        const {nombre, descripcion, activo, link, groupId} = req.body
        const report = await Report.findByPk(id)
        report.nombre = nombre
        report.descripcion = descripcion
        report.activo = activo
        report.link = link
        if (groupId) {
            report.groupId = groupId
        }
        else {
            report.groupId = report.groupId
        }
        await report.save()
        res.json(report)
    } catch (error) {
        return res.status(500).json({message: error.message})
    }
}

export const deleteReports = async (req, res) => {
    try {
        const { id } = req.params;
        const report = await Report.findByPk(id);

        if (!report) {
            return res.status(404).json({ message: 'Report not found' });
        }

        await Report.destroy({
            where: {
                id
            }
        });

        res.status(200).json({ message: 'Deleted successfully', deletedReport: report });
    } catch (error) {
        return res.status(500).json({ message: error.message });
    }
};
