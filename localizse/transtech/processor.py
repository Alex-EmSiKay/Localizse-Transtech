def add_badge(request):
    context = {
        "show_badge": request.user.messages.filter(read=False).count()
        if request.user.is_authenticated
        else False
    }
    return context
