import moonmask

class UI:

    def walk_through(self):
        print("Hey welcome, this is a little command line version of a tool called moonmask that you can use to get the current phase of the moon and use it to make a collage with other images. Press enter to continue.")
        input()
        i = input("You have a couple of options.\n\nPlease choose one of the following:\n\n(1) Get the current moonphase and open up an image of it on your computer\n\n(2) Get the current moonphase and use it to make a collage with some other images")
        if i == "1":
            m = moonmask.MoonMask()

            m.collage.set_mask()
            m.save_collage()
            #m.post_to_instagram("sadiie_parker", "Dr0w**ap!!", save_session=True)
        elif i == "2":
            input("OK, since you want to make a collage, let's get some information together.")

#ui = UI()
#ui.walk_through()

m= moonmask.MoonMask()
m.set_moon_phase()
# girl with red jacket m.set_positive_space(instagram_url="https://www.instagram.com/p/BvJV1GnBvPD/")
m.set_main_image(instagram_url="https://www.instagram.com/p/BgRtiOplAXq/")
print("https://www.instagram.com/p/BgRtiOplAXq/")
m.set_positive_space(filename="moonmask.jpg")
#m.set_main_image(url="https://lh3.googleusercontent.com/G4Dks-VYZrokqTE2z-gznMEIANmjYbiIhspCh8pn4bvW_4sjTVfllo8xyeikW5gykEIt6JzHan3piuvg5ZkkPG75Cv6YJ5T0Ue0ByvrhZJyKl8xmPjZWVRsEYRPxegcjR-Dtb_ioHwUL2Wpt0PXdHqEVPEBu0vvvmRn4BVSWX8mYffTdsWNaeSycHNDbspz-5439rIeWsrEjfnETEFeHwT7eiau1tB4tOaUGCODNzz78oQBAkVtN8u7eo-Ztgpnj7voSZCFDvNnkQAfXLpP2x7o9atZbCsz8ATi_UpTXPJqb9fP9mSW5WSkQ9aHJpWoAULX14eKKHm3n7ZXht-b1-yvQ2qjKlU3zKASam4P-e99ZBRL8BDi5koiQ2tqVDhxRKWqdqUBUfHEFsREj_Znd05Skh6CPuZM7bTSAmSzic82kVxB4zylyb7sphHy39Rz0QOvuaF8tZET5C_BBhIfiLvk5QYVg0A_zWmIBtkcFmD9Dw4wBWpcabtyxavSsmyfPoEFOsnHG3J5KNWCOqNjQK8VcGpNz7IV10-nlM28hO8ruGIKNjkQUvgqU4fKeSpo1SYeiPykAocWxuw4M-VysbTNNoBxjjLjMHqtd7d81y1eCQY50JfnTmtBngmjgP0PTgSjzQQy99ZnadDVA7ZinA-s9g5gCgcfr=w864-h648-no")
#m.set_negative_space(color="white")
# windmills m.set_main_image(url="https://lh3.googleusercontent.com/CQPY4K212wMVrnKzV0VP8eNxnkyYkmlL5liO6vKG3HauG4TbIRM9cl4PWnY1gEE6BFnpBbGYAy6OZD9fLOv8yPSkD815rgsmosuWKpQX59F8eENDxW2hd-Z-B4oXqCa2HC-7cimSNs0Qw_KCIJbsq7opQIqdT5USpcGVPdNmXwaVhOt1a9fgF-RyfowmrSBSfvpEhoB3eBrIyHL7Byw4ZwRA58EAjUFUIhw-DEVICH2vF0uJbR2spu1RHBailSWc-DFghAwAtG3QkHxM6USIdA8KBowBQrXiaVJ54JMmp3NpBKUIYlNDrL-VSQWylJFRLfQM7t28UzMvT7k9fHyIOFIZT5hs0NeUrBHFkw5TnDP625LBu-Ebh-zH72VxdgS0G5bkQ1C9X6QuasqgRwjlOsvqWwRTq7jO_TzfFU3wCLTnqXzhXyC6kO7hvy33etj2Xo02ik2kJhUFq8WA7Zy0xQs5Q1h2EqeQB8oye00KU-TqzKdi4PNFkYlARhJsT7JSU2tBwqrLt_Evxj-bMyYJd48ixP9clo3C7GOjnvkAzlolWE-sCeK8F1wbSj5SvHp14R097Ww9tSjsFEXnDVVsUaqEK38H7QNhsniEYV1D-TIgKj8HEYmwDSqlPccMQ6vleKjWBaMr71ruuRbtOQ6OD7G9Bb-FFtlH=w487-h648-no")
m.set_negative_space(color="white")
m.save_collage(negative_space_transparency=200, positive_space_transparency=255, dimensionality=1)
m.post_to_instagram("mun_fases","Dr0w**ap!!",caption="waning gibbous moon\n*\n*\n*\n*#moonphases #waninggibbous #moon #moonart #shadow #shadowselfie #selfreflection #lunar #lunart #sagittarius #sagittariusmoon #cycles #cyclical #astrology #digitalcollage #pythonimaginglibrary #python")
