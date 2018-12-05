from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from .models import Article, ArticleType
from django.conf import settings
from django.db.models import Count
from read_statistics.utils import read_statistics_once_read


# Create your views here.
def get_article_list_common_data(request, articles_all_list):
    paginator = Paginator(articles_all_list, settings.EACH_PAGE_ARTICLE_NUMBER)
    page_num = request.GET.get('page', 1)  # 获取页码参数(GET请求)
    page_of_articles = paginator.get_page(page_num)
    current_page_num = page_of_articles.number  # 获取当前页码
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(
        range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页及尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    article_dates = Article.objects.dates('created_time', 'month', order="DESC")
    article_dates_dict = {}
    for article_date in article_dates:
        article_count = Article.objects.filter(created_time__year=article_date.year,
                                               created_time__month=article_date.month).count()
        article_dates_dict[article_date] = article_count


    context = {}
    context['articles'] = page_of_articles.object_list
    context['page_of_articles'] = page_of_articles
    context['page_range'] = page_range
    context['article_types'] = ArticleType.objects.annotate(article_count=Count('article'))
    context['article_dates'] = article_dates_dict
    return context

def article_list(request):

    articles_all_list = Article.objects.all()
    context = get_article_list_common_data(request, articles_all_list)
    return render(request, 'article/article_list.html', context)

def articles_with_type(request, article_type_pk):
    article_type = get_object_or_404(ArticleType, pk=article_type_pk)
    articles_all_list = Article.objects.filter(article_type=article_type)
    context = get_article_list_common_data(request,articles_all_list)
    context['article_type'] = article_type
    return render(request, 'article/articles_with_type.html', context)

def articles_with_date(request, year, month):
    # article_type = get_object_or_404(ArticleType, pk=article_type_pk)
    articles_all_list = Article.objects.filter(created_time__year=year, created_time__month=month)
    context = get_article_list_common_data(request, articles_all_list)
    context['article_with_date'] = '%s年%s月' % (year,month)
    return render(request, 'article/articles_with_date.html', context)

def article_detail(request, article_pk):
    article = get_object_or_404(Article, id=article_pk)
    read_cookie_key = read_statistics_once_read(request, article)

    context = {}
    context['previous_article'] = Article.objects.filter(created_time__gt=article.created_time).last()
    context['next_article'] = Article.objects.filter(created_time__lt=article.created_time).first()
    context['article'] = article
    response = render(request, 'article/article_detail.html', context)
    response.set_cookie(read_cookie_key, 'true')
    return response
