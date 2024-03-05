<!DOCTYPE html>
<html lang="en">
<head>
  <style>
    .image-container {
      margin-bottom: 20px;
      text-align: center; /* 이미지 및 설명 가운데 정렬 */
    }
    .image-container img {
      display: block; /* 이미지를 블록 레벨 요소로 설정하여 다른 요소와 겹치지 않도록 함 */
      margin: 0 auto 10px; /* 이미지 아래에 여백 추가 */
      max-width: 100%; /* 이미지 최대 너비 설정 */
    }
    .image-container p {
      margin: 0; /* 설명의 상단 여백 제거 */
    }
  </style>
</head>
<body>
  <div class="image-container">
    <img src="https://github.com/Bong-HoonLee/styleTransfer/assets/115579916/82f6b63f-f521-46fe-b4b4-e6e93883d613" alt="Van Gogh Style Transfer Image 1">
    <p>target Image</p>
  </div>
  <div class="image-container">
    <img src="https://github.com/Bong-HoonLee/styleTransfer/assets/115579916/1009f16a-379c-483c-952c-b0574f6968a0" alt="Van Gogh Style Transfer Image 2">
    <p>style Image</p>
  </div>
  <div class="image-container">
    <img src="https://github.com/Bong-HoonLee/styleTransfer/assets/115579916/8511c1f0-0d0d-462b-828e-d6622aac1953" alt="Van Gogh Style Transfer Image 3">
    <p>result Image</p>
  </div>
</body>
</html>
