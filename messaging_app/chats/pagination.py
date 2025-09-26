from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    '''Set the pagination for the API to a default of 20 result per page'''

    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100