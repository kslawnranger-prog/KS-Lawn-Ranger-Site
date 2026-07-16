const nav=document.querySelector('.nav');
const menu=document.querySelector('.menu');
const links=document.querySelector('.navlinks');
const progress=document.querySelector('.progress');
const heroImage=document.querySelector('.hero-media img');
const reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const closeMenu=()=>{nav?.classList.remove('open');menu?.setAttribute('aria-expanded','false');document.body.style.overflow=''};
menu?.addEventListener('click',()=>{const open=nav.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));document.body.style.overflow=open?'hidden':''});
links?.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));

const revealObserver=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('visible');revealObserver.unobserve(entry.target)}}),{threshold:.12,rootMargin:'0px 0px -6%'});
document.querySelectorAll('.reveal').forEach(el=>revealObserver.observe(el));

document.querySelectorAll('[data-compare]').forEach(compare=>{
  const range=compare.querySelector('input');
  const before=compare.querySelector('.before');
  const line=compare.querySelector('.compare-line');
  const handle=compare.querySelector('.compare-handle');
  const update=()=>{const value=`${range.value}%`;before.style.width=value;line.style.left=value;handle.style.left=value};
  range.addEventListener('input',update);update();
});

let ticking=false;
const updateScroll=()=>{
  const y=window.scrollY;
  nav?.classList.toggle('scrolled',y>24);
  const max=document.documentElement.scrollHeight-window.innerHeight;
  if(progress)progress.style.width=`${max?Math.min(100,y/max*100):0}%`;
  if(!reduced){
    if(heroImage&&y<window.innerHeight*1.2)heroImage.style.transform=`scale(1.05) translateY(${y*.055}px)`;
    document.querySelectorAll('.project').forEach(project=>{
      const rect=project.getBoundingClientRect();
      const image=project.querySelector('.project-media img');
      if(image&&rect.top<window.innerHeight&&rect.bottom>0){
        const offset=(window.innerHeight/2-(rect.top+rect.height/2))/window.innerHeight;
        image.style.transform=`scale(1.06) translateY(${offset*24}px)`;
      }
    });
  }
  ticking=false;
};
window.addEventListener('scroll',()=>{if(!ticking){requestAnimationFrame(updateScroll);ticking=true}},{passive:true});
updateScroll();

document.querySelectorAll('a[href^="#"]').forEach(anchor=>anchor.addEventListener('click',event=>{
  const target=document.querySelector(anchor.getAttribute('href'));
  if(target){event.preventDefault();target.scrollIntoView({behavior:reduced?'auto':'smooth',block:'start'})}
}));

const form=document.querySelector('.form');
form?.addEventListener('submit',()=>{const button=form.querySelector('button');if(button){button.disabled=true;button.querySelector('span').textContent='Sending request…'}});

document.querySelectorAll('img').forEach((img,index)=>{img.decoding='async';if(index>1&&!img.closest('.hero'))img.loading='lazy'});
const year=document.getElementById('year');if(year)year.textContent=new Date().getFullYear();