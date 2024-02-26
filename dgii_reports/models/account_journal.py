from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = "account.journal"

    purchase_type = fields.Selection(
        [
            ("normal", "Compras Fiscales"),
            ("minor", "Gastos Menores"),
            ("informal", "Comprobante de Compras"),
            ("exterior", "Pagos al Exterior"),
            ("import", "Importaciones"),
            ("others", "Otros (sin NCF)"),
        ],
        string="Tipo de Compra",
        default="others",
    )

    payment_form = fields.Selection(
        [
            ("cash", "Efectivo"),
            ("bank", "Cheque / Transferencia / Depósito"),
            ("card", "Tarjeta Crédito / Débito"),
            ("credit", "A Crédito"),
            ("swap", "Permuta"),
            ("bond", "Bonos o Certificados de Regalo"),
            ("others", "Otras Formas de Venta"),
        ],
        string="Forma de Pago",
    )

    ncf_remote_validation = fields.Boolean("Validar con DGII", default=False)

    ncf_control = fields.Boolean(string="NCF Control")
