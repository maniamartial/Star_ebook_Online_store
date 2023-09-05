import frappe
#Combine different tables
from frappe.query_builder.functions import Count

def get_context(context):
    context.ebooks = frappe.get_all(
        "eBook",
        fields=[
            "name",
            "cover_image",
            "price",
            "format",
            "route",
            "creation",
            "author.full_name as author_name"
        ],
        filters={"is_published":True},
        order_by="creation desc"
    )


#The 3 Doctype To Join
EBook = frappe.qb.DocType("eBook")
Author = frappe.qb.DocType("Author")
EBookOrder=frappe.qb.DocType("eBook Orders")

querry = (
    frappe.qb.from_(EBook)
    .left_join(Author)
    .on(Author.name==EBook.author)

    .left_join(EBookOrder)
    .on((EBookOrder.ebook == EBook.name) & (EBookOrder.status=="Paid"))
    .where(EBook.is_published == True)
    .groupby(EBook.name)
    .select(
        EBook.route, EBook.cover_image,EBook.name,
        Author.full_name.as_("author_name"),
        Count(EBookOrder.name).as_("sales_count"),
    )
    .orderby(EBook.creation) #Newest book

)
ebooks = querry.run(as_dict=True)

#orders = frappe.qb.from_('eBook Orders').select('*').run(as_dict=True)


