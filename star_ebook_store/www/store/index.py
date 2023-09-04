import frappe

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


'''#Combine different tables
from frappe.query_builder.functions import Count

#The 3 Doctype To Join
EBook = frappe.get_doc("eBook")
Author = frappe.db.Doctype("Author")
EBokOrder=frappe.qb.Doctype("eBook Order")

querry = (
    frappe.db.from_(EBook)
    .left_join(Author)
    .on(Author.name==EBook.author)
    .left_join(EBokOrder)
    .on((EBokOrder.ebook == EBook.name) & (EBokOrder.statu=="Paid"))
    .where(EBokOrder.is_published == True)
    .groupby(EBook.name)
    .select(
        EBook.route, EBook.cover_image,EBook.name,
        Author.full_name.as_("author_name"),
        Count(EBokOrder.name).as_("sales_count"),
    )
    .orderby(EBook.creation) #Newest book


)
ebooks = querry.run(as_dict=True)
'''