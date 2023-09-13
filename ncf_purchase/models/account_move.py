# © 2018 Manuel Marquez <buzondemam@gmail.com>

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

from odoo import models, api


class AccountInvoice(models.Model):
    _inherit = "account.move"

    def _onchange_partner_id(self):
        res = super()._onchange_partner_id()

        if self.partner_id and self.move_type == "in_invoice":
            if self.partner_id.purchase_journal_id:
                self.journal_id = self.partner_id.purchase_journal_id

        elif self.move_type == "in_invoice" and self.env.context.get(
            "default_purchase_id"
        ):
            purchase_order = self.env["purchase.order"]
            po = purchase_order.browse(self.env.context.get("default_purchase_id"))
            supplier = po.partner_id
            if supplier.purchase_journal_id:
                self.journal_id = supplier.purchase_journal_id

        return res

    def _onchange_purchase_auto_complete(self):
        """This method is being overwritten as Odoo uses the purchase reference
        and puts it into the invoice reference (our NCF), we change this
        behaviour to use the invoice name (description)"""

        res = super()._onchange_purchase_auto_complete()

        vendor_ref = self.purchase_id.partner_ref
        if vendor_ref:
            # Here, l10n_dominicana changes self.reference to self.name
            self.name = (
                ", ".join([self.name, vendor_ref])
                if (self.name and vendor_ref not in self.name)
                else vendor_ref
            )
        return res
