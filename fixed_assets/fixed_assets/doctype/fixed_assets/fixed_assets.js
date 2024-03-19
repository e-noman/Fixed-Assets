// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.provide("erpnext.fixed_assets");
frappe.ui.form.on('Fixed Assets', {

	setup: function(frm) {
		frm.make_methods = {
			'Fixed Asset Movement': () => {
				frappe.call({
				method: "erpnext.fixed_assets.doctype.fixed_assets.fixed_assets.make_asset_movement",
				freeze: true,
				args:{
					"fixed_assets": [{ name: cur_frm.doc.name }]
				},
				callback: function (r) {
					if (r.message) {
						var doc = frappe.model.sync(r.message)[0];
						frappe.set_route("Form", doc.doctype, doc.name);
					}
				}
			});
			},
		}
	},
	// refresh: function(frm) {

	// }
});
