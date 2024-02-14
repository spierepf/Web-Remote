{% args c, ip %}
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Remote Control App | theuicode.com </title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css" integrity="sha512-KfkfwYDsLkIlwQp6LFnl8zNdLGxu9YAA1QvwINks4PhcElQSvqcyVLLD9aMhXd13uQjoXtEKNosOWaZqXgel0g==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <link rel="stylesheet" href="style.css">
</head>

<body>
    <!--container-->
    <div class="container">
        <div class="d-flex flex-row justify-content-between px-3 py-4 align-items-center">
            <i class="fas fa-chevron-left"></i>
            <span>Bat Cave - RCA TV</span>
            <i class="fas fa-ellipsis-h"></i>
        </div>

        <div class="d-flex flex-row justify-content-center">
            <div class="menu-grid">
                {{c.button("Power", "fas fa-power-off active", "ir('0x15')")}}
                {{c.button("Input", "fas fa-sign-in-alt", "ir('0x73')")}}
                {{c.button("Control", "fas fa-cog", "")}}
                {{c.button("Menu", "fas fa-bars", "ir('0x60')")}}
                {{c.button("Windows", "fa-brands fa-windows", "usb('0')")}}
                {{c.button("RPi", "fa-brands fa-raspberry-pi", "usb('1')")}}
            </div>
        </div>

        <div class="d-flex flex-row mt-4 justify-content-between px-2">
            {{c.scroll("Channel", "fas fa-chevron-up py-3 control-icon", "ir('0x10')", "fas fa-chevron-down py-3 control-icon", "ir('0x11')")}}
            <div class="d-flex flex-column align-items-center">
                <div class="d-flex flex-row grey-bg justify-content-center align-items-center">
                    <i class="fas fa-home p-3 home-icon"></i>
                </div>
                <span class="label">Home</span>
            </div>
            {{c.scroll("Volume", "fas fa-plus py-3 control-icon", "ir('0x12')", "fas fa-minus py-3 control-icon", "ir('0x13')")}}
        </div>

        <div class="mt-5 pt-4 position-relative d-flex flex-row justify-content-center align-items-center">
            <div class="circle ok-outer position-absolute"></div>
            <div class="circle ok-inner position-absolute" onclick="ir('0x36')">
                <span>OK</span>
            </div>
            <i class="fas fa-caret-right position-absolute control-icon right" onclick="ir('0x35')"></i>
            <i class="fas fa-caret-right position-absolute control-icon bottom" onclick="ir('0x75')"></i>
            <i class="fas fa-caret-right position-absolute control-icon left" onclick="ir('0x34')"></i>
            <i class="fas fa-caret-right position-absolute control-icon top" onclick="ir('0x74')"></i>
        </div>

        <div class="d-flex flex-row justify-content-between mt-5 pt-4 px-3">
            <div class="d-flex flex-row grey-bg">
                <i class="fas fa-ellipsis-h p-3 control-icon"></i>
            </div>
            <div class="d-flex flex-row grey-bg">
                <i class="fas fa-volume-mute p-3 control-icon" onclick="ir('0x14')"></i>
            </div>
        </div>
    </div>

    <script>
    function ir(cmd) {
      fetch("http://{{ip}}:8080/ir?cmd="+cmd)
    }
    function usb(select) {
      fetch("http://{{ip}}:8080/usb?select="+select)
    }
    </script>
</body>

</html>