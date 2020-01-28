# register app code
def register(request):
    user = None
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():

            customer = Customer.create("subscription",
              email = form.cleaned_data['email'],
              description = form.cleaned_data['name'],
              card = form.cleaned_data['stripe_token'],
              plan="gold",
            )

            cd = form.cleaned_data
            try:
                user = User.create(cd['name'], cd['email'], cd['password'],
                   cd['last_4_digits'])

                if customer:
                    user.stripe_id = customer.id
                    user.save()
                else:
                    UnpaidUsers(email=cd['email']).save()

            except IntegrityError:
                form.addError(cd['email'] + ' is already a member')
            else:
                request.session['user'] = user.pk
                return HttpResponseRedirect('/')

    else:
      form = UserForm()

    return render_to_response(
        'register.html',
        {
          'form': form,
          'months': range(1, 12),
          'publishable': settings.STRIPE_PUBLISHABLE,
          'soon': soon(),
          'user': user,
          'years': range(2011, 2036),
        },
        context_instance=RequestContext(request)
    )
