# Copyright 2019 Benoit Perrot
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from kuac.models.k8s.io.api.apps.v1.Deployment import Deployment
from kuac.models.k8s.io.api.apps.v1.DeploymentSpec import DeploymentSpec
from kuac.models.k8s.io.api.core.v1.Container import Container
from kuac.models.k8s.io.api.core.v1.ContainerPort import ContainerPort
from kuac.models.k8s.io.api.core.v1.PodSpec import PodSpec
from kuac.models.k8s.io.api.core.v1.PodTemplateSpec import PodTemplateSpec
from kuac.models.k8s.io.apimachinery.pkg.apis.meta.v1.LabelSelector import LabelSelector
from kuac.models.k8s.io.apimachinery.pkg.apis.meta.v1.ObjectMeta import ObjectMeta
import unittest


class Test(unittest.TestCase):

    def test_nginx_deployment(self):
        d = Deployment(
            metadata=ObjectMeta(
                name='nginx-deployment',
                labels={
                    'apps': 'nginx'
                },
            ),
            spec=DeploymentSpec(
                replicas=3,
                selector=LabelSelector({'app': 'nginx'}),
                template=PodTemplateSpec(
                    metadata=ObjectMeta(
                        labels={
                            'app': 'nginx'
                        },
                    ),
                    spec=PodSpec(
                        init_containers=[],
                        containers=[
                            Container(
                                name='nginx',
                                image='nginx:1.7.9',
                                ports=[
                                    ContainerPort(80)
                                ]
                            )
                        ]
                    )
                ),
                progress_deadline_seconds=600
            )
        )
        self.assertIsNotNone(d)


if __name__ == '__main__':
    unittest.main()
