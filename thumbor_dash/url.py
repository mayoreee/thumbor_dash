import re
import hashlib

from six import b
from libthumbor.url import Url 

AVAILABLE_HALIGN = ["left", "center", "right"]
AVAILABLE_VALIGN = ["top", "middle", "bottom"]


def calculate_width_and_height(url_parts, options):
     """Appends width and height information to url"""
     width = options.get("width", 0)
     has_width = width
     height = options.get("height", 0)
     has_height = height

     flip = options.get("flip", False)
     flop = options.get("flop", False)

     if flip:
          width = width * -1
     if flop:
          height = height * -1

     if not has_width and not has_height:
          if flip:
               width = "-0"
          if flop:
               height = "-0"

     if width or height:
          url_parts.append("%sx%s" % (width, height))


def url_for(**options):
    """Returns the url for the specified options"""

    url_parts = get_url_parts(**options)
    image_hash = hashlib.md5(b(options["image_url"])).hexdigest()
    url_parts.append(image_hash)

    return "/".join(url_parts)


def unsafe_url(**options):
    """Returns the unsafe url with the specified options"""

    return "unsafe/%s" % plain_image_url(**options)


def plain_image_url(**options):
    url_parts = get_url_parts(**options)
    url_parts.append(options["image_url"])

    return "/".join(url_parts)


def get_url_parts(**options):
     if "image_url" not in options:
          raise ValueError("The image_url argument is mandatory.")

     url_parts = []

     if options.get("meta", False):
          url_parts.append("meta")

     trim = options.get("trim", None)
     if trim:
          bits = ["trim"]
          if not isinstance(trim, bool):
               bits.append(trim[0] if trim[0] else "")
               if trim[1]:
                    bits.append(str(trim[1]))
          url_parts.append(":".join(bits))

     crop = options.get("crop", None)
     if crop:
          crop_left = crop[0][0]
          crop_top = crop[0][1]
          crop_right = crop[1][0]
          crop_bottom = crop[1][1]

          if crop_left > 0 or crop_top > 0 or crop_bottom > 0 or crop_right > 0:
               url_parts.append(
                    "%sx%s:%sx%s" % (crop_left, crop_top, crop_right, crop_bottom)
                    )

     calculate_fit_in(options, url_parts)
     calculate_width_and_height(url_parts, options)

     halign = options.get("halign", "center")
     valign = options.get("valign", "middle")

     if halign not in AVAILABLE_HALIGN:
          raise ValueError(
               'Only "left", "center" and "right" are'
               + " valid values for horizontal alignment."
               )
     if valign not in AVAILABLE_VALIGN:
          raise ValueError(
               'Only "top", "middle" and "bottom" are'
               + " valid values for vertical alignment."
               )

     if halign != "center":
          url_parts.append(halign)
     if valign != "middle":
          url_parts.append(valign)

     if options.get("smart", False):
          url_parts.append("smart")
     
     if options.get("dashauth", False):
          dashauth_string = ["dashauth"]
          for dashauth_param in options["dashauth"]:
               dashauth_string.append(dashauth_param)
          url_parts.append(":".join(dashauth_string))

     if options.get("filters", False):
          filters_string = ["filters"]
          for filter_value in options["filters"]:
               filters_string.append(filter_value)
          url_parts.append(":".join(filters_string))
     
     return url_parts


def calculate_fit_in(options, url_parts):
     fit_in = False
     full_fit_in = False

     if options.get("fit_in", None):
          fit_in = True
          url_parts.append("fit-in")

     if options.get("full_fit_in", None):
         full_fit_in = True
         url_parts.append("full-fit-in")

     if options.get("adaptive_fit_in", None):
         fit_in = True
         url_parts.append("adaptive-fit-in")

     if options.get("adaptive_full_fit_in", None):
         full_fit_in = True
         url_parts.append("adaptive-full-fit-in")

     if (fit_in or full_fit_in) and not (
         options.get("width", None) or options.get("height", None)
     ):
         raise ValueError(
              "When using fit-in or full-fit-in, you must specify width and/or height."
              )

class ThumborDashUrl(Url):

    dashauth = r"(?:dashauth:(?P<dashauth>.+?\))/)?"

    @classmethod
    def regex(cls, has_unsafe_or_hash=True):
       reg = ["/?"]

       if has_unsafe_or_hash:
            reg.append(cls.unsafe_or_hash)
       reg.append(cls.debug)
       reg.append(cls.meta)
       reg.append(cls.trim)
       reg.append(cls.crop)
       reg.append(cls.fit_in)
       reg.append(cls.dimensions)
       reg.append(cls.halign)
       reg.append(cls.valign)
       reg.append(cls.smart)
       reg.append(cls.dashauth)
       reg.append(cls.filters)
       reg.append(cls.image)
       
       return "".join(reg)

