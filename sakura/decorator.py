from sakura.models import Server as Server
from django.shortcuts import redirect


def role_required(redirect_url):

    def decorator(view_func):

        def wrap(request, *args, **kwargs):
            # print(kwargs)
            print(Server.objects.filter(**kwargs)[0])
            if str(request.user.id) in str(
                    Server.objects.filter(**kwargs)[0].owner):
                return view_func(request,
                                 Server.objects.filter(**kwargs)[0].server_id)

            elif Server.objects.filter(**kwargs)[0].admin is None:
                return redirect(redirect_url)

            elif str(request.user.id) in Server.objects.filter(
                    **kwargs)[0].admin:
                # print("pass admin")
                return view_func(request,
                                 Server.objects.filter(**kwargs)[0].server_id)

            else:
                return redirect(redirect_url)

        return wrap

    return decorator
