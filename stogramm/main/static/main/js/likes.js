  const btn = document.querySelector('.btnQQ');

  let like = true,
  likeCount = document.querySelector('.likesQQ').innerHTML;
  console.log(0);
  btn.addEventListener('click', () => {console.log(0);
    likeCount = like ? ++likeCount : --likeCount;
    like = !like;
    document.querySelector('.likesQQ').innerHTML = likeCount;
  });
