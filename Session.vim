let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd ~/Documents/WorkTasks/auto_week_report
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
let s:shortmess_save = &shortmess
if &shortmess =~ 'A'
  set shortmess=aoOA
else
  set shortmess=aoO
endif
badd +4 .gitignore
badd +3 streamlit_secrets.toml
badd +49 source/main.py
badd +94 ~/Documents/WorkTasks/auto_week_report/source/google_tools.py
badd +6 source/json_to_toml.py
badd +2 source/.gitignore
argglobal
%argdel
$argadd .gitignore
edit source/main.py
let s:save_splitbelow = &splitbelow
let s:save_splitright = &splitright
set splitbelow splitright
wincmd _ | wincmd |
split
1wincmd k
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd w
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
let &splitbelow = s:save_splitbelow
let &splitright = s:save_splitright
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe '1resize ' . ((&lines * 31 + 23) / 46)
exe 'vert 1resize ' . ((&columns * 94 + 95) / 190)
exe '2resize ' . ((&lines * 31 + 23) / 46)
exe 'vert 2resize ' . ((&columns * 95 + 95) / 190)
exe '3resize ' . ((&lines * 12 + 23) / 46)
exe 'vert 3resize ' . ((&columns * 94 + 95) / 190)
exe '4resize ' . ((&lines * 12 + 23) / 46)
exe 'vert 4resize ' . ((&columns * 95 + 95) / 190)
argglobal
balt ~/Documents/WorkTasks/auto_week_report/source/google_tools.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 50 - ((30 * winheight(0) + 15) / 31)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 50
normal! 024|
wincmd w
argglobal
if bufexists(fnamemodify("~/Documents/WorkTasks/auto_week_report/source/google_tools.py", ":p")) | buffer ~/Documents/WorkTasks/auto_week_report/source/google_tools.py | else | edit ~/Documents/WorkTasks/auto_week_report/source/google_tools.py | endif
if &buftype ==# 'terminal'
  silent file ~/Documents/WorkTasks/auto_week_report/source/google_tools.py
endif
balt source/main.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 94 - ((19 * winheight(0) + 15) / 31)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 94
normal! 055|
wincmd w
argglobal
if bufexists(fnamemodify("term://~/Documents/WorkTasks/auto_week_report//4321:/usr/bin/fish;\#toggleterm\#1", ":p")) | buffer term://~/Documents/WorkTasks/auto_week_report//4321:/usr/bin/fish;\#toggleterm\#1 | else | edit term://~/Documents/WorkTasks/auto_week_report//4321:/usr/bin/fish;\#toggleterm\#1 | endif
if &buftype ==# 'terminal'
  silent file term://~/Documents/WorkTasks/auto_week_report//4321:/usr/bin/fish;\#toggleterm\#1
endif
balt ~/Documents/WorkTasks/auto_week_report/source/google_tools.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 475 - ((11 * winheight(0) + 6) / 12)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 475
normal! 0
wincmd w
argglobal
if bufexists(fnamemodify("term://~/Documents/WorkTasks/auto_week_report//16791:/usr/bin/fish;\#toggleterm\#2", ":p")) | buffer term://~/Documents/WorkTasks/auto_week_report//16791:/usr/bin/fish;\#toggleterm\#2 | else | edit term://~/Documents/WorkTasks/auto_week_report//16791:/usr/bin/fish;\#toggleterm\#2 | endif
if &buftype ==# 'terminal'
  silent file term://~/Documents/WorkTasks/auto_week_report//16791:/usr/bin/fish;\#toggleterm\#2
endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 30 - ((5 * winheight(0) + 6) / 12)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 30
normal! 09|
wincmd w
4wincmd w
exe '1resize ' . ((&lines * 31 + 23) / 46)
exe 'vert 1resize ' . ((&columns * 94 + 95) / 190)
exe '2resize ' . ((&lines * 31 + 23) / 46)
exe 'vert 2resize ' . ((&columns * 95 + 95) / 190)
exe '3resize ' . ((&lines * 12 + 23) / 46)
exe 'vert 3resize ' . ((&columns * 94 + 95) / 190)
exe '4resize ' . ((&lines * 12 + 23) / 46)
exe 'vert 4resize ' . ((&columns * 95 + 95) / 190)
tabnext 1
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0 && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20
let &shortmess = s:shortmess_save
let &winminheight = s:save_winminheight
let &winminwidth = s:save_winminwidth
let s:sx = expand("<sfile>:p:r")."x.vim"
if filereadable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &g:so = s:so_save | let &g:siso = s:siso_save
set hlsearch
nohlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
