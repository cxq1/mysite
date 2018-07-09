from django.shortcuts import render,get_object_or_404
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data,get_today_hot_data,get_yesterday_hot_data
from blog.models import Blog
from django.utils import timezone
import datetime
from django.db.models import Sum
from django.core.cache import cache

def get_7_days_hot_blogs():
    today=timezone.now().date()
    date=today-datetime.timedelta(days=7)
    blogs=Blog.objects \
    .filter(read_details__date__lt=today,read_details__date__gte=date) \
    .values('id','title') \
    .annotate(read_num_sum=Sum('read_details__read_num')) \
    .order_by('read_num_sum')
    return blogs[:7]

def home(request):
    context={}
    blog_content_type=ContentType.objects.get_for_model(Blog)
    dates,read_nums=get_seven_days_read_data(blog_content_type)
    
    hot_data_for_7_days= cache.get('hot_data_for_7_days')
    if hot_data_for_7_days is None:
        hot_data_for_7_days=get_7_days_hot_blogs()
        cache.set('hot_data_for_7_days',hot_data_for_7_days)

    context['read_nums'] =read_nums
    context['dates']=dates
    context['today_hot_day']=get_today_hot_data(blog_content_type)
    context['yesterday_hot_day']=get_yesterday_hot_data(blog_content_type)
    context['hot_data_for_7_days']=hot_data_for_7_days
    return render(request,'home.html',context)

def index(request):
    context={}
    return render(request,'index.html',context)