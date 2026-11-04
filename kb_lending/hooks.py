app_name = "kb_lending"
app_title = "Lending"
app_publisher = "Frappe Technologies Pvt. Ltd."
app_description = "Open Source Lending software"
app_email = "contact@frappe.io"
app_license = "GNU General Public License (v3)"
required_apps = ["frappe/kb_pro"]
app_logo_url = "/assets/kb_lending/images/frappe-lending-logo.svg"

add_to_apps_screen = [
	{
		"name": "kb_lending",
		"logo": "/assets/kb_lending/images/frappe-lending-logo.svg",
		"title": "Lending",
		"route": "/app/lending",
		"has_permission": "kb_lending.utils.check_app_permission",
	}
]

audit_trail_doctypes = [
	# doctypes that make GL entries require Audit Trail to be maintained
	# as per the laws applicable to Companies in India
	"Loan Balance Adjustment",
	"Loan Disbursement",
	"Loan Interest Accrual",
	"Loan Refund",
	"Loan Repayment",
	"Loan Write Off",
]

voucher_subtypes = "kb_lending.loan_management.doctype.loan.loan.get_voucher_subtypes"

before_tests = "kb_lending.tests.test_utils.before_tests"

export_python_type_annotations = True

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/kb_lending/css/lending.css"
app_include_js = "lending.bundle.js"

# fixtures
fixtures = [
	{"dt": "Role", "filters": [["role_name", "like", "Loan %"]]},
	{"dt": "Workflow", "filters": [["name", "in", ("Loan Application Workflow", "Loan Lead Workflow")]]},
	{"dt": "Workflow State", "filters": [["name", "not in", ("Rejected", "Approved", "Pending")]]},
	{
		"dt": "Workflow Action Master",
		"filters": [["name", "not in", ("Reject", "Approve", "Review")]],
	},
]


# include js, css files in header of web template
# web_include_css = "/assets/kb_lending/css/lending.css"
# web_include_js = "/assets/kb_lending/js/lending.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "lending/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "kb_lending.utils.jinja_methods",
# 	"filters": "kb_lending.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "kb_lending.install.before_install"
after_install = "kb_lending.install.after_install"

# Uninstallation
# ------------

before_uninstall = "kb_lending.install.before_uninstall"
# after_uninstall = "lending.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "lending.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Company": {
		"validate": "kb_lending.overrides.company.validate_loan_tables",
	},
	"Sales Invoice": {
		"on_submit": [
			"kb_lending.overrides.sales_invoice.generate_demand",
			"kb_lending.overrides.sales_invoice.update_waived_amount_in_demand",
			"kb_lending.overrides.sales_invoice.make_partner_charge_gl_entries",
			"kb_lending.overrides.sales_invoice.make_suspense_gl_entry_for_charges",
		],
		"on_cancel": "kb_lending.overrides.sales_invoice.cancel_demand",
		"validate": "kb_lending.overrides.sales_invoice.validate",
	},
	"Custom Field": {
		"before_insert": "kb_lending.overrides.custom_field.update_dimensions",
	},
	"Journal Entry": {
		"on_cancel": "kb_lending.overrides.journal_entry.add_ignore_linked_doctypes_for_jv",
	},
}

accounting_dimension_doctypes = [
	"Loan",
	"Loan Disbursement",
	"Loan Interest Accrual",
	"Loan Demand",
	"Loan Repayment",
	"Loan Refund",
	"Sales Invoice",
	"Journal Entry",
]

repost_allowed_doctypes = [
	"Loan Repayment",
	"Loan Disbursement",
]
# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily_long": [
		"kb_lending.loan_management.doctype.process_loan_interest_accrual.process_loan_interest_accrual.schedule_accrual",
		"kb_lending.loan_management.doctype.process_loan_demand.process_loan_demand.process_daily_loan_demands",
		"kb_lending.loan_management.doctype.process_loan_security_shortfall.process_loan_security_shortfall.create_process_loan_security_shortfall",
		"kb_lending.loan_management.doctype.process_loan_classification.process_loan_classification.create_process_loan_classification",
		"kb_lending.loan_management.doctype.loan.loan.auto_close_loc_loans",
	],
	"monthly_long": [
		"kb_lending.loan_management.doctype.process_loan_restructure_limit.process_loan_restructure_limit.calculate_monthly_restructure_limit",
	],
	"hourly_long": [
		"kb_lending.loan_management.doctype.loan_repayment.loan_repayment.process_pending_credit_notes",
	]
}

bank_reconciliation_doctypes = [
	"Loan Repayment",
	"Loan Disbursement",
]

# Overriding Methods
# ------------------------------
get_matching_queries = "kb_lending.loan_management.utils.get_matching_queries"

get_amounts_not_reflected_in_system_for_bank_reconciliation_statement = "kb_lending.loan_management.utils.get_amounts_not_reflected_in_system_for_bank_reconciliation_statement"

get_payment_entries_for_bank_clearance = (
	"kb_lending.loan_management.utils.get_payment_entries_for_bank_clearance"
)

get_entries_for_bank_clearance_summary = (
	"kb_lending.loan_management.utils.get_entries_for_bank_clearance_summary"
)

get_entries_for_bank_reconciliation_statement = (
	"kb_lending.loan_management.utils.get_entries_for_bank_reconciliation_statement"
)

# ERPNext doctypes for Global Search
global_search_doctypes = {
	"Default": [
		{"doctype": "Loan", "index": 44},
	],
}

update_gl_dict_with_app_based_fields = ["kb_lending.overrides.gl_entry.update_value_date_in_gl_dict"]

#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "lending.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["kb_lending.utils.before_request"]
# after_request = ["kb_lending.utils.after_request"]

# Job Events
# ----------
# before_job = ["kb_lending.utils.before_job"]
# after_job = ["kb_lending.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"lending.auth.validate"
# ]

workflow_methods = [
	{
		"name": "Convert to Loan Application",
		"method": "kb_lending.loan_origination.doctype.loan_lead.loan_lead.convert_to_loan_application"
	}
]