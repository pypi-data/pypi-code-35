depends = ('ITKPyBase', 'ITKRegistrationCommon', 'ITKOptimizersv4', 'ITKCommon', )
templates = (
  ('CorrelationImageToImageMetricv4', 'itk::CorrelationImageToImageMetricv4', 'itkCorrelationImageToImageMetricv4IF2IF2', True, 'itk::Image< float,2 >, itk::Image< float,2 >'),
  ('CorrelationImageToImageMetricv4', 'itk::CorrelationImageToImageMetricv4', 'itkCorrelationImageToImageMetricv4IF3IF3', True, 'itk::Image< float,3 >, itk::Image< float,3 >'),
  ('DemonsImageToImageMetricv4', 'itk::DemonsImageToImageMetricv4', 'itkDemonsImageToImageMetricv4IF2IF2', True, 'itk::Image< float,2 >, itk::Image< float,2 >'),
  ('DemonsImageToImageMetricv4', 'itk::DemonsImageToImageMetricv4', 'itkDemonsImageToImageMetricv4IF3IF3', True, 'itk::Image< float,3 >, itk::Image< float,3 >'),
  ('ImageToImageMetricv4', 'itk::ImageToImageMetricv4', 'itkImageToImageMetricv4F2F2', True, 'itk::Image< float, 2 >, itk::Image< float, 2 >'),
  ('ImageToImageMetricv4', 'itk::ImageToImageMetricv4', 'itkImageToImageMetricv4F3F3', True, 'itk::Image< float, 3 >, itk::Image< float, 3 >'),
  ('JointHistogramMutualInformationImageToImageMetricv4', 'itk::JointHistogramMutualInformationImageToImageMetricv4', 'itkJointHistogramMutualInformationImageToImageMetricv4IF2IF2', True, 'itk::Image< float,2 >, itk::Image< float,2 >'),
  ('JointHistogramMutualInformationImageToImageMetricv4', 'itk::JointHistogramMutualInformationImageToImageMetricv4', 'itkJointHistogramMutualInformationImageToImageMetricv4IF3IF3', True, 'itk::Image< float,3 >, itk::Image< float,3 >'),
  ('MattesMutualInformationImageToImageMetricv4', 'itk::MattesMutualInformationImageToImageMetricv4', 'itkMattesMutualInformationImageToImageMetricv4IF2IF2', True, 'itk::Image< float,2 >, itk::Image< float,2 >'),
  ('MattesMutualInformationImageToImageMetricv4', 'itk::MattesMutualInformationImageToImageMetricv4', 'itkMattesMutualInformationImageToImageMetricv4IF3IF3', True, 'itk::Image< float,3 >, itk::Image< float,3 >'),
  ('MeanSquaresImageToImageMetricv4', 'itk::MeanSquaresImageToImageMetricv4', 'itkMeanSquaresImageToImageMetricv4IF2IF2', True, 'itk::Image< float,2 >, itk::Image< float,2 >'),
  ('MeanSquaresImageToImageMetricv4', 'itk::MeanSquaresImageToImageMetricv4', 'itkMeanSquaresImageToImageMetricv4IF3IF3', True, 'itk::Image< float,3 >, itk::Image< float,3 >'),
)
