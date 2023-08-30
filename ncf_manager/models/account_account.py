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


class AccountAccount(models.Model):
    _inherit = "account.account"

    income_type = fields.Selection(
        [
            ("01", "01 - Ingresos por operaciones (No financieros)"),
            ("02", "02 - Ingresos Financieros"),
            ("03", "03 - Ingresos Extraordinarios"),
            ("04", "04 - Ingresos por Arrendamientos"),
            ("05", "05 - Ingresos por Venta de Activo Depreciable"),
            ("06", "06 - Otros Ingresos"),
        ],
        string="Tipo de Ingreso",
    )

    expense_type = fields.Selection(
        [
            ("01", "01 - Gastos de Personal"),
            ("02", "02 - Gastos por Trabajo, Suministros y Servicios"),
            ("03", "03 - Arrendamientos"),
            ("04", "04 - Gastos de Activos Fijos"),
            ("05", "05 - Gastos de Representación"),
            ("06", "06 - Otras Deducciones Admitidas"),
            ("07", "07 - Gastos Financieros"),
            ("08", "08 - Gastos Extraordinarios"),
            ("09", "09 - Compras y Gastos que forman parte del Costo de Venta"),
            ("10", "10 - Adquisiciones de Activos"),
            ("11", "11 - Gastos de Seguros"),
        ],
        string="Tipo de Costos y Gastos",
    )

    @api.onchange("user_type_id")
    def onchange_user_type_id(self):
        self.income_type = False
        self.expense_type = False
