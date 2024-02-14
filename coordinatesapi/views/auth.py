from coordinatesapi.models import Planner
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def check_user(request):
    '''Checks to see if User has Associated Gamer

    Method arguments:
      request -- The full HTTP request object
    '''
    uid = request.data['uid']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    planner = Planner.objects.filter(uid=uid).first()

    # If authentication was successful, respond with their token
    if planner is not None:
        data = {
            'id': planner.id,
            'first_name': planner.first_name,
            'last_name': planner.last_name,
            'email': planner.email,
            "phone_number": planner.phone_number,
            'uid': planner.uid
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)


@api_view(['POST'])
def register_user(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Now save the user info in the levelupapi_gamer table
    planner = Planner.objects.create(
        first_name=request.data['firstName'],
        last_name=request.data["lastName"],
        email=request.data['email'],
        phone_number=request.data["phoneNumber"],
        uid=request.data['uid'],
    
    )

    # Return the gamer info to the client
    data = {
        'id': planner.id,
        'first_name': planner.first_name,
        'last_name': planner.last_name,
        'email': planner.email,
        "phone_number": planner.phone_number,
        'uid': planner.uid
    }
    return Response(data)
