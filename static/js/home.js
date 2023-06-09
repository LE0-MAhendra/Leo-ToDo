window.addEventListener("load", revealtext);

function revealtext() {
  const TLFade = gsap.timeline();
  TLFade.from(".title", { autoAlpha: 0, y: -50, delay: 0.2 })
    .from(".desc", { autoAlpha: 0, y: -50 }, "-=0.2")
    .from(".btns", { autoAlpha: 0, y: -50 }, "-=0.2");
}
