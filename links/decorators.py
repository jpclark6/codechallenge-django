from rest_framework.response import Response
from rest_framework.views import status


def validate_request_data(fn):
  def decorated(*args, **kwargs):
    link = args[0].request.data.get("link", "")
    if not link:
      return Response(
        data={
          "error": "Link not created"
        },
        status=status.HTTP_400_BAD_REQUEST
      )
    return fn(*args, **kwargs)
  return decorated