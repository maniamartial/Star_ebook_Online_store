import frappe
from frappe.query_builder import DocType
from frappe.querry_builder.functions import Count
from pypika.terms import Case

webPageView = DocType("Web Page View")
#similar to
#webPageView =frappe.qb.DocType("Web Page View")
count_all = Count('*').as_("count")

#case used for conditional logic
case = Case().when(webPageView.is_unique == "1", "1")
count_is_unique = Count(case).as_("unique_count")

result = (
    frappe.qb.from_(webPageView)
    .select(webPageView.path, count_all, count_is_unique)
    .where(Web_Page_View.creation[some_date:same_later_date])
).run()