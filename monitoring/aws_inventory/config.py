# A dictionary of AWS classes
# {
#    AWS SDK CLASS, i.e. ec2, s3: {
#                                     service, i.e. ec2 instance, ebs, eip: {
#                                                                               'method'  : Method call to obtain inventory, i.e. describe_instances
#                                                                               'key'     : Key of the return result
#                                                                               'subkey'  : 2nd level key of the result, i.e. ec2 returns result['Reservations']['Instances']
#                                                                               'filter'  : Sometime, we don't need all the results.  filter can be used to narrow down returned values
#                                                                               'dataset' : Desired data to be print to the result.txt

AWS_CLASSES={
    'ec2': {
             'instance': {
                            'method': 'describe_instances',
                            'key'  :  'Reservations',
                            'subkey': 'Instances',
                            'dataset': ['InstanceId', 'LaunchTime', 'State', 'region']
                           },
             'network_interface': {
                                  'method': 'describe_network_interfaces',
                                  'key': 'NetworkInterfaces',
                                  'filter': {
                                              'key': 'Status',
                                              'value': 'in-use'
                                            },
                                  'dataset': ['NetworkInterfaceId', 'RequesterId', 'Status', 'region']
                                },
             'ebs': {
                      'method': 'describe_volumes',
                      'key':  'Volumes',
                      'dataset': ['VolumeId', 'CreateTime', 'State', 'Size', 'region']
                    },
             'eip': {
                      'method': 'describe_addresses',
                      'key': 'Addresses',
                      'dataset': ['PublicIp', 'region']
                    }
            },
    'batch': {
               'batch_job': {
                              'method': 'describe_job_definitions',
                              'key': 'jobDefinitions',
                              'dataset': ['jobDefinitionName', 'status', 'region']
                            }
              },

    'lightsail': {
                   'lightsail_instance': {
                                           'method': 'get_instances',
                                           'key': 'instances',
                                           'dataset': ['name', 'state', 'region']
                                         },
                   'lightsail_loadbalancer': {
                                               'method': 'get_load_balancers',
                                               'key': 'loadBalancers',
                                               'dataset': ['name', 'state', 'region']
                                             }
                 },
    'lambda': {
                'lambda_function': {
                                     'method': 'list_functions',
                                     'key': 'Functions',
                                     'dataset': ['FunctionName', 'state', 'region']
                                   }
              },
    'autoscaling': {
                     'autoscaling_group': {
                                            'method': 'describe_auto_scaling_groups',
                                            'key': 'AutoScalingGroups',
                                            'dataset': ['AutoScalingGroupName', 'Status', 'region']
                                          },
                     'autoscaling_lb':     {
                                             'method': 'describe_load_balancers',
                                             'key': 'LoadBalancers',
                                             'dataset': ['LoadBalancerName', 'state', 'region']
                                           },
                     'autoscaling_instances': {
                                             'method': 'describe_launch_instances',
                                             'key': 'AutoScalingInstances',
                                             'dataset': ['InstanceId', 'LifecycleState', 'region']
                                           }
                   },
    'eks': {
             'eks_cluster': {
                              'method': 'list_clusters',
                              'key': 'cluster',
                              'dataset': ['name', 'createdAt', 'status', 'region']
                            }
           },
    'ecs': {
             'ecs_cluster': {
                              'method': 'describe_clusters',
                              'key': 'clusters',
                              'dataset': ['clusterName', 'status', 'activeServicesCount', 'runningTasksCount', 'region']
                            },
             'ecs_service': {
                              'method': 'describe_services',
                              'key': 'services',
                              'dataset': ['serviceName', 'status', 'runningCount', 'region']
                            }
              },
    'elasticbeanstalk': {
                          'beanstalk_environment': {
                                                     'method': 'describe_environments',
                                                     'key': 'Environments',
                                                      'dataset': ['EnvironmentName', 'ApplicationName', 'DateCreated', 'Status', 'region']
                                                   },
                          'beanstalk_applicatoin': {
                                                     'method': 'describe_applications',
                                                     'key': 'Applications',
                                                      'dataset': ['ApplicationName', 'DateCreated', 'region']
                                                   }
                        },
    'efs': {
             'efs': {
                      'method': 'describe_file_systems',
                      'key': 'FileSystems',
                      'dataset': ['Name', 'SizeInBytes', 'region']
                    }
           },
    's3': {
            's3' 
          },
    'rds': {
             'rds': {
                      'method': 'describe_db_instances',
                      'key': 'DBInstances',
                      'dataset': ['DBName', 'AllocatedStorage', 'InstanceCreateTime', 'region']
                    }
           },
    'dynamodb': {
                  'dynamodb': {
                                'method': 'describe_tables',
                                'key': 'TableNames',
                                'dataset': ['TableName', 'BillingModeSummary', 'region']
                              }
                },
    'neptune': {
                 'neptune': {
                              'method': 'describe_db_clusters',
                              'key': 'DBClusters',
                              'dataset': ['DatabaseName', 'Status', 'region']
                            }
               },
    'redshift': {
                  'redshift_cluster': {
                                        'method': 'describe_clusters',
                                        'key': 'Clusters',
                                        'dataset': ['DBName', 'DBName', 'region']
                                      },
                  'redshift_nodes':   {
                                        'method': 'describe_reserved_nodes',
                                        'key': 'ReservedNodes',
                                        'dataset': ['ReservedNodeId', 'UsagePrice', 'NodeCount', 'region']
                                      }
                },
    'elasticache': {
                  'elasticache_cluster': {
                                           'method': 'describe_cache_clusters',
                                           'key': 'CacheClusters',
                                           'dataset': ['CacheClusterId', 'CacheClusterStatus', 'NumCacheNodes', 'region']
                                         },
                  'elasticache_nodes':   {
                                           'method': 'describe_reserved_cache_nodes',
                                           'key': 'ReservedCacheNodes',
                                           'dataset': ['ReservedCacheNodeId', 'UsagePrice', 'CacheNodeCount', 'region']
                                         }
                   }

}
