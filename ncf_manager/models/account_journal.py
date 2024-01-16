# © 2018 Gustavo Valverde <gustavo@iterativo.do>
# © 2018 Eneldo Serrata <eneldo@marcos.do>
# © 2018 Andrés Rodríguez <andres@iterativo.do>

# This file is part of NCF Manager.

# NCF Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# NCF Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with NCF Manager.  If not, see <https://www.gnu.org/licenses/>.

from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = "account.journal"

    sequence_id = fields.Many2one(comodel_name="ir.sequence", string="Sequence")

    @api.depends("ncf_control")
    def check_ncf_ready(self):
        for record in self:
            record.ncf_ready = len(record.date_range_ids) > 1

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

    ncf_control = fields.Boolean(related="sequence_id.ncf_control", readonly=False)
    prefix = fields.Char(related="sequence_id.prefix", readonly=False)
    date_range_ids = fields.One2many(
        related="sequence_id.date_range_ids", readonly=False
    )
    ncf_ready = fields.Boolean(compute=check_ncf_ready)
    special_fiscal_position_id = fields.Many2one(
        "account.fiscal.position",
        string="Posición fiscal para regímenes especiales.",
        help="Define la posición fiscal por defecto para los clientes que \
               tienen definido el tipo de comprobante fiscal regímenes \
               especiales.",
    )

    @api.onchange("type")
    def onchange_type(self):
        if self.type != "sale":
            self.ncf_control = False

    def create_ncf_sequence(self):
        if self.ncf_control and len(self.sequence_id.date_range_ids) <= 1:
            # this method read Selection values from res.partner
            # sale_fiscal_type fields
            selection = self.env[
                "ir.sequence.date_range"
            ].get_sale_fiscal_type_from_partner()
            for sale_fiscal_type in selection:
                self.sequence_id.date_range_ids[0].copy(
                    {"sale_fiscal_type": sale_fiscal_type[0]}
                )

            self.sequence_id.date_range_ids.invalidate_cache()


class AccountTax(models.Model):
    _inherit = "account.tax"

    @api.model
    def _get_isr_retention_type(self):
        return [
            ("01", "Alquileres"),
            ("02", "Honorarios por Servicios"),
            ("03", "Otras Rentas"),
            ("04", "Rentas Presuntas"),
            ("05", "Intereses Pagados a Personas Jurídicas"),
            ("06", "Intereses Pagados a Personas Físicas"),
            ("07", "Retención por Proveedores del Estado"),
            ("08", "Juegos Telefónicos"),
        ]

    purchase_tax_type = fields.Selection(
        [
            ("itbis", "ITBIS Pagado"),
            ("ritbis", "ITBIS Retenido"),
            ("isr", "ISR Retenido"),
            ("rext", "Pagos al Exterior (Ley 253-12)"),
            ("none", "No Deducible"),
        ],
        default="none",
        string="Tipo de Impuesto en Compra",
    )

    isr_retention_type = fields.Selection(
        selection=_get_isr_retention_type, string="Tipo de Retención en ISR"
    )
