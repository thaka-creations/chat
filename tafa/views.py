import timeit
from queue import Queue

from django.http import JsonResponse

from utility import async_util


# Create your views here.
def async_view():
    que = Queue()
    users = [
    ]
    _ = [
        que.put_nowait(
            {
                'method': 'GET',
                'url': 'https://test/validate-tax-payer-details',
                'payload': user
            }
        )
        for user in users
    ]

    del _

    res = async_util.process_async(que)
    print("response", res)


def time_to_fetch(request):
    execution_time = timeit.timeit(stmt=async_view, number=1)
    return JsonResponse({'execution_time': execution_time})


def generate_template(request):
    return JsonResponse({'name': 'nelfrank junior', 'id': 30692526})
