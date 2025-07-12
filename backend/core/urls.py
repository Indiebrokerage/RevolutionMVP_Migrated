from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("sell-my-home", views.sell_home, name="sell-my-home"),
    path("saveAdsAnalytics", views.save_ads_analytics, name="saveAdsAnalytics"),
    path("saveContact", views.save_contact, name="saveContact"),
    path("save-mortagage-calculations", views.save_mortgage_calculation, name="save-mortagage"),
    path("get-mortagage-calculations", views.get_mortgage_calculation, name="get-mortagage"),
    path("property-search", views.property_search, name="property-search"),
    path("propertyFilter", views.property_filter, name="propertyFilter"),
    path("agent-list", views.agent_list, name="agent-list"),
    path("contact-agent/<int:user_id>", views.contact_agent, name="contactagent"),
    path("compare_property", views.compare_property, name="ajax.compare_property_route"),
    path("favorite-agent", views.favorite_agent_toggle, name="favoriteagent"),
    path("agent-detail/<int:user_id>/<str:agent_name>", views.agent_detail, name="agentDetail"),
    path("agent-detail/<int:user_id>", views.agent_detail, name="agentDetail"), # Optional agentname
    path("property-fav/<int:property_id>", views.mark_favorite_property, name="property.favProperty"),
    path("contact-us", views.contact_us_create, name="contact-us"),
    path("contact-us/save", views.contact_us_store, name="contact-us/save"),
    path("savesearchuser", views.save_search, name="savesearchurl"),
    path("property-info", views.property_more_info, name="property-info"),
    path("property-info-window", views.property_info_window, name="property-info-window"),
    path("vendor-info-window", views.vendor_info_window, name="vendor-info-window"),
    path("property/latlongs", views.get_lat_longs, name="get.latlongs"),
    path("vendors/coordinates", views.get_lat_longs_vendors, name="get.latlongsvendors"),
    path("property/default-latlongs", views.property_filter_default_latlongs, name="get.latlongs.default"),
    path("auto-complete-address", views.auto_complete_address, name="get.autoaddress"),
    path("auto-complete-school", views.auto_complete_school, name="get.autoSchools"),
    path("property-detail/<int:property_id>/<str:mls_number>/<str:address>", views.property_detail, name="property-detail"),
    path("property-detail/<int:property_id>/<str:mls_number>", views.property_detail, name="property-detail"), # Optional address
    path("vendor-list", views.vendor_list, name="vendor-list"),
    path("vendor-list/<str:keyword>", views.vendor_list, name="vendor-list"), # Optional keyword
    path("vendor-detail/<int:user_id>/<str:name>", views.vendor_detail, name="vendorDetail"),
    path("vendor-detail/<int:user_id>", views.vendor_detail, name="vendorDetail"), # Optional name
    path("favorite-vendor", views.favorite_vendor, name="favoriteVendor"),
    path("contact-vendor-coordinates", views.contact_vendor_coordinates, name="vendorcoordinates"),
    path("contact-vendor", views.contact_vendor, name="contact-vendor"),
    path("vendor-blog-detail/<int:news_id>/<str:news_name>", views.news_detail, name="news-detail"),
    path("vendor-blog-detail/<int:news_id>", views.news_detail, name="news-detail"), # Optional news_name
    path("blog", views.blog_list, name="blog-list"),
    path("blog/<slug:slug>", views.blog_detail, name="blog-detail"),
    path("list-awards/<int:user_id>", views.list_awards, name="listAwards"),
    path("list-projects/<int:user_id>", views.list_projects, name="listProjects"),
    path("saveproject", views.save_project, name="saveproject"),
    path("projects-detail/<int:user_id>/<int:project_id>", views.projects_detail, name="projectsDetail"),
    path("reviewme/<int:user_id>/<str:name>", views.review_me, name="reviewme"),
    path("reviewme/<int:user_id>", views.review_me, name="reviewme"), # Optional name
    path("postReviewme", views.review_me_post, name="postReviewme"),
    path("browseReviews/<int:user_id>/<str:name>", views.browse_reviews, name="browseReviews"),
    path("browseReviews/<int:user_id>", views.browse_reviews, name="browseReviews"), # Optional name
    path("commentReview", views.comment_review, name="commentReview"),
    path("list-qa/<int:user_id>", views.list_qa, name="listQA"),
    path("vendor-list-blog/<int:user_id>", views.list_news, name="listNews"),
    path("vendor-detail-log/<int:user_id>/<int:news_id>", views.detail_news, name="detailNews"),
    path("like-review", views.like_review, name="likeReview"),
    path("ckeditor", views.ckeditor_view, name="ckeditor"),
    path("<slug:slug>", views.content_index, name="content.index"),
]


